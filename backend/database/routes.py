import uuid
from typing import Any, List

from app.settings import DATABASE
from beanie.odm.operators.update.array import Pull, Push
from bson.objectid import ObjectId
from fastapi import responses, status
from fastapi.param_functions import Body, Depends
from fastapi.routing import APIRouter
from starlette.responses import Response
from users.models import User
from users.routes import USER_AUTH
from utils import encode_document

from .models import Collection, Field

router = APIRouter()

# returns a list of all the collections which this
# user has the permission to read


@router.get("/collection", tags=["database"], response_model=List[Collection])
async def get_collections(
    user: User = Depends(USER_AUTH.get_current_user)
):
    return await Collection.all().to_list()


# create the collection, if the user has permission to create
# collection
@router.post("/collection", tags=["database"], status_code=status.HTTP_201_CREATED)
async def create_collection(
    collection: Collection = Body(...),
    user: User = Depends(USER_AUTH.get_current_user)
):
    await collection.insert()


# add fields to the collection, if the user has permission to write
# collection
@router.post("/collection/add_fields", tags=["database"])
async def add_fields(
    collection_id: str = Body(...),
    fields: List[Field] = Body(...),
    user: User = Depends(USER_AUTH.get_current_user)
):
    collection = await Collection.get(collection_id)
    for field in fields:
        await collection.update(Push({Collection.fields: field.dict()}))
    return collection


# remove fields to the collection, if the user has permission to write
# collection
@router.post("/collection/remove_fields", tags=["database"])
async def remove_fields(
    collection_id: str = Body(...),
    field_ids: List[str] = Body(...),
    user: User = Depends(USER_AUTH.get_current_user)
):
    collection = await Collection.get(collection_id)
    await collection.update({"$pull": {Collection.fields: {"id": {"$in": list(map(uuid.UUID, field_ids))}}}})
    return collection


# add data to the collection, if the user has permission to write
# collection
@router.post("/collection/add_data", tags=["database"], status_code=status.HTTP_201_CREATED)
async def add_data(
    collection_id: str = Body(...),
    data: dict = Body(...),
    user: User = Depends(USER_AUTH.get_current_user)
):
    collection = await Collection.get(collection_id)
    user_collection = DATABASE[collection.name]
    user_collection.insert_one(data)
    return {"details": "Success"}


# get all data from the collection,
# if the user has permission to read collection
@router.post("/collection/get_data", tags=["database"])
async def get_data(
    collection_id: str = Body(..., embed=True),
    user: User = Depends(USER_AUTH.get_current_user)
):
    collection = await Collection.get(collection_id)
    user_collection = DATABASE[collection.name]
    data = []
    async for d in user_collection.find():
        data.append(encode_document(d))
    return data


# get single data matching data id from the collection,
# if the user has permission to read collection
@router.post("/collection/get_data_one", tags=["database"])
async def get_data_one(
    response: Response,
    collection_id: str = Body(...),
    data_id: str = Body(...),
    user: User = Depends(USER_AUTH.get_current_user),
):
    collection = await Collection.get(collection_id)
    user_collection = DATABASE[collection.name]
    document = await user_collection.find_one({'_id': ObjectId(data_id)})
    if not document:
        response.status_code = status.HTTP_404_NOT_FOUND
        return
    return encode_document(document=document)


# delete data from the collection, if the user has permission to write
# collection
@router.post("/collection/delete_data", tags=["database"])
async def delete_data(
    collection_id: str = Body(...),
    data_id: str = Body(...),
    user: User = Depends(USER_AUTH.get_current_user)
):
    collection = await Collection.get(collection_id)
    user_collection = DATABASE[collection.name]
    user_collection.delete_many({'_id': ObjectId(data_id)})
    return {"details": "Success"}
