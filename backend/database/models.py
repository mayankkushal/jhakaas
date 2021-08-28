from typing import List, Optional
from uuid import UUID, uuid1

from beanie.odm.documents import Document
from beanie.odm.fields import Indexed
from pydantic.main import BaseModel


class FieldType:
    STRING = "string"
    BOOL = "boolean"
    NULL = "null"


class Field(BaseModel):
    id: Optional[UUID]
    name: str
    type: Optional[str]
    indexed: bool = False


class Collection(Document):
    name: Indexed(str, unique=True)
    is_strict: bool = False
    fields: Optional[List[Field]] = []
