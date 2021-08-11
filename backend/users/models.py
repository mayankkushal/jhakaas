# --- Users Collection Schema Setup -------------------------------------------

# Pydantic models for MongoDB "User" collection schema
# Learn more at https://frankie567.github.io/fastapi-users/configuration/model/
from fastapi_users import models


class User(models.BaseUser):
    """
        Fields "id", "is_active" and "is_superuser" are created by this model

        Modify the below lines to add more fields for the user

        WARNING: You must also modify the same lines in the
        UserCreate model below
    """

    firstName: str
    lastName: str


class UserCreate(models.BaseUserCreate):
    """
        Fields "email" and "password" are created by this model

        Modify the below lines to add more fields for the user

        WARNING: You must also modify the same lines in the
        User model above
    """

    firstName: str
    lastName: str


class UserUpdate(User, models.BaseUserUpdate):
    """
        This class Extends/Inherits the User class
    """
    pass


class UserDB(User, models.BaseUserDB):
    """
        This class Extends/Inherits the User class

        Field "hashed_password" is created by this model
    """
    pass
