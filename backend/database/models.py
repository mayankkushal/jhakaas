from typing import List, Optional
from uuid import UUID, uuid4

from beanie.odm.documents import Document
from beanie.odm.fields import Indexed
from pydantic.main import BaseModel


class FieldType:
    STRING = "string"
    BOOL = "boolean"
    NULL = "null"


class Field(BaseModel):
    id: UUID = uuid4()
    name: str
    type: Optional[str]
    indexed: bool = False


class Collection(Document):
    name: Indexed(str, unique=True)
    is_strict: bool = True
    fields: List[Field]
