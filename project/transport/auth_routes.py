from datetime import timedelta

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from project.config import Config
from project.dal.retailer import RetailerRepository
from project.dtos.auth import Token, AuthData
from project.logger import Logger
from project.services.auth.auth_service import AuthService

config = Config()
logger = Logger()

router = APIRouter()
retailer_repository = RetailerRepository(config, logger)

auth_service = AuthService(config, logger, retailer_repository)


@router.post("/auth/token/", response_model=Token)
def login_for_access_token(auth_data: AuthData) -> Token:
    retailer = auth_service.authenticate_retailer(
        email=auth_data.email, password=auth_data.password
    )

    if not retailer:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=int(config.get_config("ACCESS_TOKEN_EXPIRE_MINUTES"))
    )
    access_token = auth_service.generate_access_token(
        data={"sub": retailer.email}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")
