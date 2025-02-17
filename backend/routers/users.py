from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import ValidationError
from utils.auth import get_hashed_password, verify_password, create_access_token, create_refresh_token
from repository.user import UserRepository
from schemas.user_schema import UserBase, UserAuth
from schemas.auth_schema import TokenSchema
from fastapi.security import OAuth2PasswordRequestForm
from deps.user_deps import get_current_user
from schemas.auth_schema import TokenPayload
from typing import Union, Any
from jose import jwt
from datetime import datetime, timezone
from dotenv import load_dotenv
import os

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_REFRESH_SECRET_KEY = os.getenv("JWT_REFRESH_SECRET_KEY")
ALGORITHM = "HS256"

UTC = timezone.utc  # Definir UTC manualmente

router = APIRouter()

@router.post('/signup', summary="Create new user", status_code=status.HTTP_201_CREATED)
async def create_user(data: UserAuth):
    """
    Create a new user while checking if the user already exists.
    The password is stored encrypted.
    """
    user_repo = UserRepository()
    user = user_repo.user_exists(data.email)

    if user:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    try:
        data.password = get_hashed_password(data.password)
        user = user_repo.create_user(data)
        return {'message': 'User created'}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                             detail=f'An error occurred while creating the user: {e}')
    

@router.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login the user.
    """
    try:
        user_repo = UserRepository()
        
        user = user_repo.user_exists(form_data.username)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect email"
            )

        hashed_pass = user_repo.get_user_password_by_email(form_data.username)

        if not verify_password(form_data.password, hashed_pass):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect password"
            )

        user = user_repo.get_user_by_email(form_data.username)

        return {
            "access_token": create_access_token(user['email']),
            "refresh_token": create_refresh_token(user['email']),
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= f'An error occurred while creating the user: {e}'
        )


@router.get('/me', summary='Get details of currently logged in user', response_model=UserBase)
async def get_me(user: UserBase = Depends(get_current_user)):
    return user


@router.post('/refresh_token', summary='Create new access token using refresh token', response_model=TokenSchema)
async def refresh_token(token: str):
    try:
        payload = jwt.decode(
            token, JWT_REFRESH_SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp, tz=UTC) < datetime.now(UTC):
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_repo = UserRepository()
    user: Union[dict[str, Any], None] = user_repo.get_user_by_email(token_data.sub)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return {
        "access_token": create_access_token(user['email']),
        "refresh_token": create_refresh_token(user['email']),
    }
