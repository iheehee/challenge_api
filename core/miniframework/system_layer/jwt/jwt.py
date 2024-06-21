import datetime
import os
import time

import jwt

from core.miniframework.exc import TokenExpiredError

# JWT_KEY = os.environ.get("JWT_KEY")
JWT_KEY = "ckFXaWtRWENtSTA2QnpGVmxWNlBySWF4cUk1Q1pxbHU="
# JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM")
JWT_ALGORITHM = "HS256"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def write_jwt(issue: str, audience: str, expire_len: int):
    raw_data = dict()

    raw_data["iss"] = issue
    raw_data["email"] = audience

    iat = datetime.datetime.now()
    exp = iat + datetime.timedelta(seconds=expire_len * 60)
    raw_data["iat"] = time.mktime(iat.timetuple())
    raw_data["exp"] = time.mktime(exp.timetuple())
    return jwt.encode(raw_data, JWT_KEY, JWT_ALGORITHM)


def read_jwt(jwt_token: str):
    # check jwt
    decoded_data = jwt.decode(jwt_token, JWT_KEY, algorithms=[JWT_ALGORITHM])
    issue = decoded_data["iss"]
    audience = decoded_data["email"]
    expired_date = decoded_data["exp"]

    # 만료 확인
    if time.time() > expired_date:
        raise TokenExpiredError("token expired")

    return issue, audience
