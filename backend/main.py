#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import uvicorn
from beanie.odm.utils.general import init_beanie
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import settings
from database.models import Collection
from database.routes import router as database_router
from users.models import Token, User
from users.routes import USER_AUTH
from users.routes import router as users_router

# --- FastAPI Server Initialization -------------------------------------------

# Learn more https://frankie567.github.io/fastapi-users/configuration/routers/

# Initiating FastAPI Server
app = FastAPI(title="JHAKAAS", version="0.0.1")

# Managing CORS for the React Frontend connections

origins = [
    "http://localhost",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["x-total-count"]
)


async def connect_db():
    await init_beanie(database=settings.DATABASE,
                      document_models=[Token, Collection])


# @app.on_event("startup")
# async def on_startup():
#     """
#     Initialize benie on app startup
#     """


app.add_event_handler("startup", connect_db)

# Add all the routers here
app.include_router(users_router)
app.include_router(database_router)


# --- Custom Unprotected Routes Template --------------------------------------

"""
    The below templates can be used for creating any Rest APIs that are
    independent of user's authenticaion state (logged in or logged out).
    
    Hence, these API calls don't necessarily require a user to be logged in.

    Please read Mongo Motor docs to perform async DB operations.
    Learn more https://motor.readthedocs.io/en/stable/
"""


@app.get("/custom-unprotected-route", tags=["unprotected-routes"])
async def get_custom_unprotected_route():
    # Add database CRUD operation logic here
    return "Success!"


@app.post("/custom-unprotected-route", tags=["unprotected-routes"])
async def post_custom_unprotected_route(
    body: dict
):
    # Add database CRUD operation logic here
    print(body)
    return "Success!"


# --- Custom Protected Routes Template ----------------------------------------

"""
    The below templates can be used for creating any Rest APIs that mandatorily
    require the user to be in logged in state. Such as getting user specific
    information.

    Please read Mongo Motor docs to perform async DB operations.
    Learn more https://motor.readthedocs.io/en/stable/
"""


@app.get("/custom-protected-route", tags=["protected-routes"])
async def get_custom_protected_route(
    user: User = Depends(USER_AUTH.get_current_user)
):
    # Add database CRUD operation logic here
    return "Success!"


@app.post("/custom-protected-route", tags=["protected-routes"])
async def post_custom_protected_route(
    body: dict,
    user: User = Depends(USER_AUTH.get_current_user)
):
    # Add database CRUD operation logic here
    print(body)
    return "Success!"


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8888)
