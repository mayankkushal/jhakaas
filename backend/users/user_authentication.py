from typing import Any, Callable, Dict, Optional, Sequence, Type

from fastapi import APIRouter, Request
from fastapi_users import FastAPIUsers, models

from users.crud import get_users_router
from users.verify import get_verify_router

from .reset import get_reset_password_router


class UserAuthentication(FastAPIUsers):
    def get_reset_password_router(
        self,
        after_forgot_password: Optional[
            Callable[[models.UD, str, Request], None]
        ] = None,
        after_reset_password: Optional[Callable[[
            models.UD, Request], None]] = None,
    ) -> APIRouter:
        """
        Return a reset password process router.

        :param reset_password_token_secret: Secret to encode reset password token.
        :param reset_password_token_lifetime_seconds: Lifetime of reset password token.
        :param after_forgot_password: Optional function called after a successful
        forgot password request.
        :param after_reset_password: Optional function called after a successful
        password reset.
        """
        return get_reset_password_router(
            self.db,
            after_forgot_password,
            after_reset_password,
            self.validate_password,
        )

    def get_verify_router(
        self,
        after_verification_request: Optional[
            Callable[[models.UD, str, Request], None]
        ] = None,
        after_verification: Optional[Callable[[
            models.UD, Request], None]] = None,
    ) -> APIRouter:
        """
        Return a router with e-mail verification routes.

        :param verification_token_secret: Secret to encode verification token.
        :param verification_token_lifetime_seconds: Lifetime verification token.
        :param after_verification_request: Optional function called after a successful
        verify request.
        :param after_verification: Optional function called after a successful
        verification.
        """
        return get_verify_router(
            self.verify_user,
            self.get_user,
            self._user_model,
            after_verification_request,
            after_verification,
        )

    def get_users_router(
        self,
        after_update: Optional[
            Callable[[models.UD, Dict[str, Any], Request], None]
        ] = None,
        requires_verification: bool = False,
    ) -> APIRouter:
        """
        Return a router with routes to manage users.

        :param after_update: Optional function called
        after a successful user update.
        :param requires_verification: Whether the endpoints
        require the users to be verified or not.
        """
        return get_users_router(
            self.db,
            self._user_model,
            self._user_update_model,
            self._user_db_model,
            self.authenticator,
            after_update,
            requires_verification,
            self.validate_password,
        )
