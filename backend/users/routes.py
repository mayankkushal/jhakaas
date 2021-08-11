# --- User Authentication Routes ----------------------------------------------
import settings
from fastapi import APIRouter, Request, Response
from fastapi.params import Depends

from users.models import UserDB

router = APIRouter()


@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}

# Add route for Login                           POST "/auth/login"
router.include_router(
    settings.USER_AUTH.get_auth_router(settings.auth_backends[0]),
    prefix="/auth/jwt",
    tags=["auth"]
)

# Route to refresh JWT token


@router.post("/auth/jwt/refresh", tags=["auth"])
async def refresh_jwt(response: Response, user=Depends(settings.USER_AUTH.get_current_active_user)):
    return await settings.jwt_authentication.get_login_response(user, response)


# Add route for Registration                   POST "/auth/register"

# Below function can be used to init any backend process like sending out a
# successful registration email


def on_after_register(user: UserDB, request: Request):
    print("User {user.id} has registered.")


router.include_router(
    # fastapi_users.get_register_router(),
    settings.USER_AUTH.get_register_router(on_after_register),
    prefix="/auth",
    tags=["auth"]
)

# Add route for User utilities "/auth/users/*"

""" 
    Get current logged in user profile          GET "/auth/users/me"
    Update current logged in user profile       PATCH "/auth/users/me"
    Get "_id" user profile                      GET "/auth/users/"
    Update "_id" user profile                   PATCH "/auth/users/{id}"
    Delete "_id" user profile                   DELETE "/auth/users/{id}" 
"""

router.include_router(
    settings.USER_AUTH.get_users_router(),
    prefix="/auth/users",
    tags=["auth"]
)

# Add route for Reset Password utility

"""
    Forgot Password                             POST /auth/users/forgot-password
    Reset Password                              POST /auth/users/reset-password                         
"""

router.include_router(
    settings.USER_AUTH.get_reset_password_router("SECRET"),
    prefix="/auth/users",
    tags=["auth"]
)
