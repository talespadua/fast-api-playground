from datetime import timedelta, datetime
from typing import Optional, cast, Dict, Any

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError  # type: ignore[import]
from starlette import status

from project.config import Config
from project.dal.retailer import RetailerRepository
from project.dtos.retailer import RetailerOutputDTO
from project.dtos.auth import TokenData
from project.logger import Logger
from project.libs.criptography.password_handler import verify_password
from project.mappers.retailer_mappers import convert_model_to_output_dto

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthService:
    def __init__(
        self, config: Config, logger: Logger, retailer_repository: RetailerRepository
    ) -> None:
        self.config = config
        self.logger = logger
        self.retailer_repository = retailer_repository

    def authenticate_retailer(
        self, email: str, password: str
    ) -> Optional[RetailerOutputDTO]:
        retailer_model = self.retailer_repository.get_retailer_by_email(email)
        if not retailer_model:
            return None
        if not verify_password(password, retailer_model.password):
            return None
        return convert_model_to_output_dto(retailer_model)

    def get_current_retailer(
        self, token: str = Depends(oauth2_scheme)
    ) -> Optional[RetailerOutputDTO]:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token,
                self.config.get_config("SECRET_KEY"),
                algorithms=[self.config.get_config("ALGORITHM")],
            )
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
            token_data = TokenData(email=email)
        except JWTError:
            raise credentials_exception

        retailer_model = self.retailer_repository.get_retailer_by_email(
            token_data.email
        )

        if not retailer_model:
            raise credentials_exception
        return convert_model_to_output_dto(retailer_model)

    def generate_access_token(
        self, data: Dict[str, Any], expires_delta: timedelta
    ) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            self.config.get_config("SECRET_KEY"),
            algorithm=self.config.get_config("ALGORITHM"),
        )
        return cast(str, encoded_jwt)
