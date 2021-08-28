import os
from re import DEBUG

import motor.motor_asyncio
from beanie import init_beanie
from dotenv import load_dotenv
from users.models import Token

load_dotenv()

# Secret Key (must be changed from "SECRET")
SECRET = os.getenv("SECRET", "RANDOM")
DEBUG = bool(os.getenv("DEBUG", False))

print("Running with DEBUG", DEBUG)

# --- MongoDB Setup -----------------------------------------------------------

MONGO_HOST = os.environ.get("MONGO_HOST", "localhost")
MONGO_PORT = int(os.environ.get("MONGO_PORT", 27017))
MONGO_USER = os.environ.get("MONGO_USER", "admin")
MONGO_PASS = os.environ.get("MONGO_PASSWORD", "pass")
MONGO_DB = os.environ.get("MONGO_DB", "jhakaasDB")

# MONGODB_URL = DatabaseURL(
#     f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"
# )

# MongoDB Configurations
DATABASE_URL = "mongodb://localhost:27017"
if not DEBUG:
    DATABASE_URL = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}"
client = motor.motor_asyncio.AsyncIOMotorClient(
    DATABASE_URL, uuidRepresentation="standard"
)
# MongoDB database instance ("DB" by default, can be changed)
DATABASE = client[MONGO_DB]

# MongoDB collection instance ("users" by default, can be changed)
USER_COLLECTION = DATABASE["users"]
TOKEN_COLLECTION = DATABASE['token']
