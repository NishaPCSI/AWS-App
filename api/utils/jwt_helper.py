import jwt
from typing import Any, Dict
import datetime
from fastapi import HTTPException, Request

SECRET_KEY = "testfornow"
EXPIRE_DELTA = 720

def gen_time(mins: int):
    return datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=mins)

def create_jwt(data):
    # add all the data and insert expiry time
    data.update({
        'exp': gen_time(EXPIRE_DELTA),
        'iat': gen_time(0)
    })
    # encode and return the JWT token
    return jwt.encode(data, SECRET_KEY, algorithm='HS256')