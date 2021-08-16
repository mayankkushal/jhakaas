from typing import Callable, Optional

import jwt
from app.settings import DATABASE, TOKEN_COLLECTION
from fastapi import APIRouter, Body, HTTPException, Request, status
from fastapi_users import models
from fastapi_users.db import BaseUserDatabase
from fastapi_users.password import get_password_hash
from fastapi_users.router.common import ErrorCode, run_handler
from fastapi_users.user import (InvalidPasswordException,
                                ValidatePasswordProtocol)
from fastapi_users.utils import JWT_ALGORITHM, generate_jwt
from pydantic import UUID4, EmailStr
from utils import token_generator

from users.models import Token

RESET_PASSWORD_TOKEN_AUDIENCE = "fastapi-users:reset"


def get_reset_password_router(
    user_db: BaseUserDatabase[models.BaseUserDB],
    reset_password_token_secret: str,
    reset_password_token_lifetime_seconds: int = 3600,
    after_forgot_password: Optional[Callable[[
        models.UD, str, Request], None]] = None,
    after_reset_password: Optional[Callable[[
        models.UD, Request], None]] = None,
    validate_password: Optional[ValidatePasswordProtocol] = None,
) -> APIRouter:
    """Generate a router with the reset password routes."""
    router = APIRouter()

    @router.post("/forgot-password", status_code=status.HTTP_202_ACCEPTED)
    async def forgot_password(
        request: Request, email: EmailStr = Body(..., embed=True)
    ):
        user = await user_db.get_by_email(email)

        if user is not None:
            token = Token(user_id=user.id)
            await token.insert()
            if after_forgot_password:
                await run_handler(after_forgot_password, user, token.token, request)

        return None

    @router.post("/reset-password")
    async def reset_password(
        request: Request, token: str = Body(...), password: str = Body(...), email: str = Body(...)
    ):
        try:
            user = await user_db.get_by_email(email)
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=ErrorCode.RESET_PASSWORD_BAD_TOKEN,
                )

            token_document = await Token.find_one(Token.user_id == user.id, Token.is_used == False, Token.token == token)
            if not token_document:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=ErrorCode.RESET_PASSWORD_BAD_TOKEN,
                )
            await token_document.set({Token.is_used: True})

            if user is None or not user.is_active:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=ErrorCode.RESET_PASSWORD_BAD_TOKEN,
                )

            if validate_password:
                try:
                    await validate_password(password, user)
                except InvalidPasswordException as e:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail={
                            "code": ErrorCode.RESET_PASSWORD_INVALID_PASSWORD,
                            "reason": e.reason,
                        },
                    )

            user.hashed_password = get_password_hash(password)
            await user_db.update(user)
            if after_reset_password:
                await run_handler(after_reset_password, user, request)
        except jwt.PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.RESET_PASSWORD_BAD_TOKEN,
            )

    return router
