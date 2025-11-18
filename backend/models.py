from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """Modèle pour la requête de login"""
    username: str = Field(..., description="Nom d'utilisateur")
    password: str = Field(..., description="Mot de passe")

    class Config:
        json_schema_extra = {
            "example": {
                "username": "admin",
                "password": "password123"
            }
        }


class LoginResponse(BaseModel):
    """Modèle pour la réponse de login"""
    access_token: str = Field(..., description="Token JWT d'accès")
    token_type: str = Field(default="bearer", description="Type de token")

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }


class ErrorResponse(BaseModel):
    """Modèle pour les réponses d'erreur"""
    detail: str = Field(..., description="Message d'erreur")

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Nom d'utilisateur ou mot de passe incorrect"
            }
        }


class PredictRequest(BaseModel):
    """Modèle pour la requête de prédiction de sentiment"""
    text: str = Field(..., description="Texte à analyser", min_length=1)

    class Config:
        json_schema_extra = {
            "example": {
                "text": "Très bon film, je le recommande vivement!"
            }
        }


class PredictResponse(BaseModel):
    """Modèle pour la réponse de prédiction de sentiment"""
    text: str = Field(..., description="Texte analysé")
    sentiment: list = Field(..., description="Résultat de l'analyse de sentiment")

    class Config:
        json_schema_extra = {
            "example": {
                "text": "Très bon film, je le recommande vivement!",
                "sentiment": [[
                    {"label": "5 stars", "score": 0.8},
                    {"label": "4 stars", "score": 0.15},
                    {"label": "3 stars", "score": 0.03},
                    {"label": "2 stars", "score": 0.01},
                    {"label": "1 star", "score": 0.01}
                ]]
            }
        }
