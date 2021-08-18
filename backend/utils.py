import random
import string
from typing import Union


def token_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def encode_document(document: Union[dict]):
    if isinstance(document, dict):
        return {"id": str(document.pop('_id')), **document}
    doc_dict = document.dict()
    return {"id": str(doc_dict.pop('id')), **doc_dict}
