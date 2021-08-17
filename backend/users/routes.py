# --- User Authentication Routes ----------------------------------------------
from app import settings
from fastapi import APIRouter, Request, Response
from fastapi.params import Depends
from fastapi_users.authentication.jwt import JWTAuthentication

from users.models import User, UserCreate, UserDB, UserUpdate
from users.user_authentication import UserAuthentication
from users.userdb import MongoDBUserDatabase

router = APIRouter()

# --- FastAPIUsers Object Declaration -----------------------------------------

# MongoDB "users" collection adaptor for API calls
user_db = MongoDBUserDatabase(UserDB, settings.USER_COLLECTION)

# Authentication Method JWT
auth_backends = []
jwt_authentication = JWTAuthentication(
    secret=settings.SECRET, lifetime_seconds=3600)
auth_backends.append(jwt_authentication)

# FastAPI Users helper class with all the configurations from above
# It provides us all the routes
USER_AUTH = UserAuthentication(
    user_db,
    auth_backends,
    User,
    UserCreate,
    UserUpdate,
    UserDB
)


@router.get("/users/", tags=["users"])
async def read_users(response: Response):
    users = await user_db.get_all(as_dict=True)
    response.headers['X-Total-Count'] = str(len(users))
    return users


@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}

# Add route for Login                           POST "/auth/jwt/login"
router.include_router(
    USER_AUTH.get_auth_router(auth_backends[0]),
    prefix="/auth/jwt",
    tags=["auth"]
)

# Route to refresh JWT token


@router.post("/auth/jwt/refresh", tags=["auth"])
async def refresh_jwt(response: Response, user=Depends(USER_AUTH.get_current_active_user)):
    return await jwt_authentication.get_login_response(user, response)


# Add route for Registration                   POST "/auth/register"

# Below function can be used to init any backend process like sending out a
# successful registration email


def on_after_register(user: UserDB, request: Request):
    print("User {user.id} has registered.")


router.include_router(
    USER_AUTH.get_register_router(on_after_register),
    prefix="/auth",
    tags=["auth"]
)


# send email or sms of the token to verify account
def on_after_verification_request(user: UserDB, token: str, request: Request):
    pass


router.include_router(
    USER_AUTH.get_verify_router(on_after_verification_request),
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
    USER_AUTH.get_users_router(),
    prefix="/auth/users",
    tags=["auth"]
)


# Add route for Reset Password utility

"""
    Forgot Password                             POST /auth/users/forgot-password
    Reset Password                              POST /auth/users/reset-password                         
"""


# send email or sms of the token to reset password
def on_after_forgot_password(user: UserDB, token: str, request: Request):
    pass


router.include_router(
    USER_AUTH.get_reset_password_router(on_after_forgot_password),
    prefix="/auth/users",
    tags=["auth"]
)
