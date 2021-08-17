import random
import string


def token_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def encode_document(document: dict):
    return {"_id": str(document.pop('_id')), **document}
