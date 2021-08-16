from typing import Callable, Optional, Type, cast

import jwt
from fastapi import APIRouter, Body, HTTPException, Request, status
from fastapi_users import models
from fastapi_users.router.common import ErrorCode, run_handler
from fastapi_users.user import (GetUserProtocol, UserAlreadyVerified,
                                UserNotExists, VerifyUserProtocol)
from fastapi_users.utils import JWT_ALGORITHM, generate_jwt
from pydantic import UUID4, EmailStr

from .models import Token

VERIFY_USER_TOKEN_AUDIENCE = "fastapi-users:verify"


def get_verify_router(
    verify_user: VerifyUserProtocol,
    get_user: GetUserProtocol,
    user_model: Type[models.BaseUser],
    after_verification_request: Optional[
        Callable[[models.UD, str, Request], None]
    ] = None,
    after_verification: Optional[Callable[[models.UD, Request], None]] = None,
):
    router = APIRouter()

    @router.post("/request-verify-token", status_code=status.HTTP_202_ACCEPTED)
    async def request_verify_token(
        request: Request, email: str = Body(..., embed=True)
    ):
        try:
            user = await get_user(email)
            if not user.is_verified and user.is_active:
                token = Token(user_id=user.id)
                await token.insert()
                if after_verification_request:
                    await run_handler(after_verification_request, user, token.token, request)
        except UserNotExists:
            pass

        return None

    @router.post("/verify", response_model=user_model)
    async def verify(request: Request, token: str = Body(..., embed=True), email: str = Body(...)):
        try:
            user_check = await get_user(email)
        except UserNotExists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.VERIFY_USER_BAD_TOKEN,
            )

        token_document = await Token.find_one(Token.user_id == user_check.id, Token.is_used == False, Token.token == token)
        if not token_document:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.VERIFY_USER_BAD_TOKEN,
            )
        await token_document.set({Token.is_used: True})

        try:
            user = await verify_user(user_check)
        except UserAlreadyVerified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.VERIFY_USER_ALREADY_VERIFIED,
            )

        if after_verification:
            await run_handler(after_verification, user, request)

        return user

    return router
