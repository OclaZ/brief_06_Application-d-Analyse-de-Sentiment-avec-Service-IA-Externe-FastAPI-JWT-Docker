from fastapi import APIRouter, HTTPException, status
from datetime import timedelta
from auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from models import LoginRequest, LoginResponse, ErrorResponse

router = APIRouter(tags=["Authentication"])


# Base de données utilisateurs en mémoire (pour la démo)
# En production, utilisez une vraie base de données avec mots de passe hashés
FAKE_USERS_DB = {
    "admin": {
        "username": "admin",
        "password": "password123",
        "email": "admin@example.com"
    },
    "user": {
        "username": "user",
        "password": "userpass",
        "email": "user@example.com"
    }
}


def authenticate_user(username: str, password: str):
    """
    Authentifie un utilisateur

    Args:
        username: Nom d'utilisateur
        password: Mot de passe en clair

    Returns:
        Les données de l'utilisateur si authentification réussie, False sinon
    """
    user = FAKE_USERS_DB.get(username)
    if not user:
        return False
    if user["password"] != password:
        return False
    return user


@router.post(
    "/login",
    response_model=LoginResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Authentification échouée"}
    },
    summary="Authentification utilisateur",
    description="Authentifie un utilisateur et retourne un token JWT"
)
def login(credentials: LoginRequest):
    """
    Endpoint de login

    Reçoit un nom d'utilisateur et un mot de passe, et retourne un JWT si les
    identifiants sont valides.

    - **username**: Nom d'utilisateur
    - **password**: Mot de passe

    Retourne un token JWT valide pendant 30 minutes.
    """
    # Authentification de l'utilisateur
    user = authenticate_user(credentials.username, credentials.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nom d'utilisateur ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Création du token JWT
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"], "email": user["email"]},
        expires_delta=access_token_expires
    )

    return LoginResponse(
        access_token=access_token,
        token_type="bearer"
    )
