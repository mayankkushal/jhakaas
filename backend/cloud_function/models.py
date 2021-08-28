from typing import Optional
from uuid import UUID, uuid1

from beanie.odm.documents import Document
from beanie.odm.fields import Indexed
from pydantic.main import BaseModel


class FunctionCode(Document):
    name: Indexed(str, unique=True)
    is_async: bool = False
    code: Optional[str]
