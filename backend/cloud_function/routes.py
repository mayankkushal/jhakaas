import uuid
from typing import Any, List, Union

from app.settings import DATABASE
from beanie.odm.operators.update.array import Pull, Push
from bson.objectid import ObjectId
from fastapi import status
from fastapi.param_functions import Body, Depends
from fastapi.routing import APIRouter
from pydantic.types import UUID4
from pydantic.utils import Obj
from pymongo.helpers import DuplicateKeyError
from starlette.responses import Response
from starlette.status import HTTP_400_BAD_REQUEST
from users.models import User
from users.routes import USER_AUTH
from utils import encode_document

from .models import FunctionCode

router = APIRouter()

# returns a list of all the collections which this
# user has the permission to read


@router.get("/cloud_function", tags=["cloud_function"])
async def get_cloud_functions(
    response: Response,
    user: User = Depends(USER_AUTH.get_current_user)
):
    response.headers['X-Total-Count'] = str(await FunctionCode.count())
    return list(map(encode_document, await FunctionCode.all().to_list()))


@router.get(
    "/cloud_function/{id:str}",
    tags=["cloud_function"]
)
async def get_cloud_function(id: str, user: User = Depends(USER_AUTH.get_current_user)):
    function_code = await FunctionCode.get(id)
    return encode_document(function_code)


@router.put(
    "/cloud_function/{id:str}",
    tags=["cloud_function"]
)
async def update_cloud_function(id: str, data: FunctionCode = Body(...), user: User = Depends(USER_AUTH.get_current_user)):
    function_code = await FunctionCode.get(id)
    data_dict = data.dict()
    del data_dict['id']
    await function_code.set(data_dict)
    return function_code.dict()


@router.delete(
    "/cloud_function/{id:str}",
    tags=["cloud_function"]
)
async def delete_cloud_function(id: str, user: User = Depends(USER_AUTH.get_current_user)):
    code = await FunctionCode.get(id)
    await code.delete()
    return code.dict()


@router.post("/cloud_function", tags=["cloud_function"], status_code=status.HTTP_201_CREATED)
async def create_cloud_function(
    response: Response,
    function_code: FunctionCode = Body(...),
    user: User = Depends(USER_AUTH.get_current_user)
):
    await function_code.insert()
    return function_code.dict()


@router.post("/cloud_function/{id:str}/run", tags=["cloud_function"])
async def run_function(
    id: str,
    response: Response,
    user: User = Depends(USER_AUTH.get_current_user)
):
    function_code = await FunctionCode.get(id)
    scope = {**globals()}
    exec(function_code.code, scope)
    try:
        if function_code.is_async:
            return await scope['run']()
        return scope['run']()
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": str(e)}
