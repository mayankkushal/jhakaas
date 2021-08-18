import uuid
from typing import Any, List, Union

from app.settings import DATABASE
from beanie.odm.operators.update.array import Pull, Push
from bson.objectid import ObjectId
from fastapi import status
from fastapi.param_functions import Body, Depends
from fastapi.routing import APIRouter
from pydantic.types import UUID4
from pymongo.helpers import DuplicateKeyError
from starlette.responses import Response
from starlette.status import HTTP_400_BAD_REQUEST
from users.models import User
from users.routes import USER_AUTH
from utils import encode_document

from .models import Collection, Field

router = APIRouter()

# returns a list of all the collections which this
# user has the permission to read


@router.get("/collection", tags=["database"])
async def get_collections(
    response: Response,
    user: User = Depends(USER_AUTH.get_current_user)
):
    response.headers['X-Total-Count'] = str(await Collection.count())
    return list(map(encode_document, await Collection.all().to_list()))


@router.get(
    "/collection/{id:str}",
    tags=["database"]
)
async def get_collection(id: str, user: User = Depends(USER_AUTH.get_current_user)):
    collection = await Collection.get(id)
    return encode_document(collection)


@router.get(
    "/collection/{id:str}/fields",
    tags=["database"]
)
async def get_fields(id: str, response: Response, user: User = Depends(USER_AUTH.get_current_user)):
    collection = await Collection.get(id)
    response.headers['X-Total-Count'] = str(len(collection.fields))
    f = list(map(encode_document, collection.fields))
    return f


@router.put(
    "/collection/{id:str}",
    tags=["database"]
)
async def update_collection(id: str, collection: Collection = Body(...), user: User = Depends(USER_AUTH.get_current_user)):
    collection = await Collection.get(id)
    return encode_document(collection)

# create the collection, if the user has permission to create
# collection


@router.post("/collection", tags=["database"], status_code=status.HTTP_201_CREATED)
async def create_collection(
    response: Response,
    collection: Collection = Body(...),
    user: User = Depends(USER_AUTH.get_current_user)
):
    try:
        await collection.insert()
        # create a collection with this name
        # mainly we are focused on creating the indexed fields
        # other fields can be added later
        user_collection = DATABASE[collection.name]
        for field in collection.fields:
            if field.indexed:
                user_collection.create_index(field.name)
        return {"details": "Success"}
    except DuplicateKeyError:
        response.status_code = HTTP_400_BAD_REQUEST
        return {"detail": "Duplicate collection name"}


# delete collection, if the user has permission to write
# collection
@router.delete("/collection/{id:str}", tags=["database"])
async def delete_collection(
    response: Response,
    id: str,
    user: User = Depends(USER_AUTH.get_current_user)
):
    DATABASE.drop_collection(id)
    # await Collection.get(id).delete()


# add fields to the collection, if the user has permission to write
# collection
@router.post("/collection/{id:str}/field/add", tags=["database"])
async def add_fields(
    id: str,
    fields: Union[List[Field], Field] = Body(...),
    user: User = Depends(USER_AUTH.get_current_user)
):
    collection = await Collection.get(id)
    user_collection = DATABASE[collection.name]
    if isinstance(fields, list):
        for field in fields:
            await collection.update(Push({Collection.fields: {**fields.dict(), "id": uuid.uuid1()}}))
            # if the fields are to be indexed, create index for them
            if field.indexed:
                user_collection.create_index(field.name)
    else:
        await collection.update(Push({Collection.fields: {**fields.dict(), "id": uuid.uuid1()}}))
        if fields.indexed:
            user_collection.create_index(fields.name)
    return collection


# remove fields to the collection, if the user has permission to write
# collection
@router.delete("/collection/{collection_id:str}/field/{field_id:str}", tags=["database"])
async def remove_fields(
    collection_id: str,
    field_id: str,
    user: User = Depends(USER_AUTH.get_current_user)
):
    collection = await Collection.get(collection_id)
    await collection.update({"$pull": {Collection.fields: {"id": {"$eq": uuid.UUID(field_id)}}}})
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
    return {"detail": "Success"}


# get all data from the collection,
# if the user has permission to read collection
@router.get("/collection/get_data", tags=["database"])
async def get_data(
    response: Response,
    collection_name: str,
    user: User = Depends(USER_AUTH.get_current_user)
):
    collection = await Collection.find_one(Collection.name == collection_name)
    if not collection:
        response.status_code = HTTP_400_BAD_REQUEST
        return {"detail": "Invalid collection name"}
    user_collection = DATABASE[collection.name]
    data = []
    async for d in user_collection.find():
        data.append(encode_document(d))
    return data


# get single data matching data id from the collection,
# if the user has permission to read collection
@router.get("/collection/get_data_one", tags=["database"])
async def get_data_one(
    response: Response,
    collection_name: str,
    data_id: str,
    user: User = Depends(USER_AUTH.get_current_user),
):
    collection = await Collection.find_one(Collection.name == collection_name)
    if not collection:
        response.status_code = HTTP_400_BAD_REQUEST
        return {"detail": "Invalid collection name"}
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
    response: Response,
    collection_name: str = Body(...),
    data_id: str = Body(...),
    user: User = Depends(USER_AUTH.get_current_user)
):
    collection = await Collection.find_one(Collection.name == collection_name)
    if not collection:
        response.status_code = HTTP_400_BAD_REQUEST
        return {"detail": "Invalid collection name"}
    user_collection = DATABASE[collection.name]
    user_collection.delete_many({'_id': ObjectId(data_id)})
    return {"detail": "Success"}
