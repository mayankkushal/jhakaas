import motor.motor_asyncio
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.db import MongoDBUserDatabase

from users.models import User, UserCreate, UserDB, UserUpdate

# Secret Key (must be changed from "SECRET")
SECRET = "SECRET"

# --- MongoDB Setup -----------------------------------------------------------

# MongoDB Configurations
DATABASE_URL = "mongodb://localhost:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(
    DATABASE_URL, uuidRepresentation="standard"
)
# MongoDB database instance ("DB" by default, can be changed)
database = client["jhakaasDB"]

# MongoDB users collection instance ("users" by default, can be changed)
user_collection = database["users"]


# --- FastAPIUsers Object Declaration -----------------------------------------

# MongoDB "users" collection adaptor for API calls
user_db = MongoDBUserDatabase(UserDB, user_collection)

# Authentication Method JWT
auth_backends = []
jwt_authentication = JWTAuthentication(secret=SECRET, lifetime_seconds=3600)
auth_backends.append(jwt_authentication)


# FastAPI Users helper class with all the configurations from above
# It provides us all the routes
USER_AUTH = FastAPIUsers(
    user_db,
    auth_backends,
    User,
    UserCreate,
    UserUpdate,
    UserDB
)
