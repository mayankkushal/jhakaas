from typing import List, Optional
from uuid import UUID, uuid4

from beanie.odm.documents import Document
from pydantic.main import BaseModel


class FieldType:
    STRING = "string"
    BOOL = "boolean"
    NULL = "null"


class Field(BaseModel):
    id: UUID = uuid4()
    name: str
    type: Optional[str]


class Collection(Document):
    name: str
    is_strict: bool = True
    fields: List[Field]
