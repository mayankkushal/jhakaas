import motor.motor_asyncio

# Secret Key (must be changed from "SECRET")
SECRET = "SECRET"

# --- MongoDB Setup -----------------------------------------------------------

# MongoDB Configurations
DATABASE_URL = "mongodb://localhost:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(
    DATABASE_URL, uuidRepresentation="standard"
)
# MongoDB database instance ("DB" by default, can be changed)
DATABASE = client["jhakaasDB"]

# MongoDB users collection instance ("users" by default, can be changed)
USER_COLLECTION = DATABASE["users"]
