from fastapi import APIRouter, HTTPException, status, Depends
import os
import httpx
from typing import List, Dict, Any
from models import PredictRequest, PredictResponse, ErrorResponse
from auth import verify_token

router = APIRouter(tags=["Sentiment Analysis"])


# Configuration Hugging Face API
API_URL = "https://router.huggingface.co/hf-inference/models/nlptown/bert-base-multilingual-uncased-sentiment"
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
TIMEOUT = 30.0  # Timeout en secondes


def validate_api_key() -> str:
    """
    Valide que la clé API Hugging Face est configurée

    Returns:
        La clé API

    Raises:
        HTTPException: Si la clé API n'est pas configurée
    """
    if not HUGGINGFACE_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Clé API Hugging Face non configurée. Veuillez configurer HUGGINGFACE_API_KEY dans le fichier .env"
        )
    return HUGGINGFACE_API_KEY


def query_huggingface(text: str) -> List[List[Dict[str, Any]]]:
    """
    Appelle l'API Hugging Face pour analyser le sentiment d'un texte

    Args:
        text: Texte à analyser

    Returns:
        Résultat de l'analyse de sentiment

    Raises:
        HTTPException: Si l'API Hugging Face ne répond pas correctement
    """
    # Validation de la clé API
    api_key = validate_api_key()

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {"inputs": text}

    try:
        with httpx.Client(timeout=TIMEOUT) as client:
            response = client.post(API_URL, headers=headers, json=payload)

            # Gestion des différents codes d'erreur HTTP
            if response.status_code == 401:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Clé API Hugging Face invalide ou expirée"
                )
            elif response.status_code == 429:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Limite de requêtes API Hugging Face atteinte. Veuillez réessayer plus tard"
                )
            elif response.status_code == 503:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Le modèle Hugging Face est en cours de chargement. Veuillez réessayer dans quelques instants"
                )
            elif response.status_code >= 500:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=f"Erreur serveur Hugging Face (code {response.status_code})"
                )

            # Lever une exception pour les autres codes d'erreur
            response.raise_for_status()

            # Vérifier que la réponse est valide
            result = response.json()
            if not isinstance(result, list):
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Réponse invalide de l'API Hugging Face"
                )

            return result

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail=f"Timeout lors de l'appel à l'API Hugging Face (>{TIMEOUT}s)"
        )
    except httpx.NetworkError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Erreur réseau lors de l'appel à l'API Hugging Face: {str(e)}"
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Erreur HTTP {e.response.status_code} de l'API Hugging Face"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Erreur inattendue lors de l'appel à l'API Hugging Face: {str(e)}"
        )


@router.post(
    "/predict",
    response_model=PredictResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Requête invalide"},
        401: {"model": ErrorResponse, "description": "Token invalide ou expiré"},
        500: {"model": ErrorResponse, "description": "Clé API Hugging Face non configurée"},
        503: {"model": ErrorResponse, "description": "Service Hugging Face non disponible"},
        504: {"model": ErrorResponse, "description": "Timeout lors de l'appel à l'API Hugging Face"}
    },
    summary="Analyse de sentiment",
    description="Analyse le sentiment d'un texte en utilisant l'API Hugging Face Inference (authentification requise)"
)
def predict(request: PredictRequest, token_data: dict = Depends(verify_token)):
    """
    Endpoint de prédiction de sentiment (protégé par JWT)

    Reçoit un texte et retourne l'analyse de sentiment effectuée par l'API Hugging Face.
    Nécessite un token JWT valide dans l'en-tête Authorization.

    - **text**: Texte à analyser (minimum 1 caractère)

    Retourne le texte analysé et les résultats de l'analyse de sentiment.
    """
    if not request.text or not request.text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le texte ne peut pas être vide"
        )

    # Appel à l'API Hugging Face
    sentiment_result = query_huggingface(request.text)

    return PredictResponse(
        text=request.text,
        sentiment=sentiment_result
    )
