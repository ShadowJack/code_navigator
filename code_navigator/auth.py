import secrets
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import os

security = HTTPBasic()

class VerifyCredentials:
    def __init__(self):
        correct_username = os.environ.get("AUTH_USERNAME")
        correct_password = os.environ.get("AUTH_PASSWORD")
        if correct_username == None or correct_password == None :
            # Authentication is not required
            self._skip_auth = True
            return

        self._skip_auth = False
        self._username = correct_username.encode("utf8")
        self._password = correct_password.encode("utf8")

    async def __call__(self, request: Request) -> bool:
        if self._skip_auth:
            return True

        credentials = await security(request)
        if credentials == None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Basic authorization is required",
                headers={"WWW-Authenticate": "Basic"},
            )
        current_username_bytes = credentials.username.encode("utf8")
        is_correct_username = secrets.compare_digest(
            current_username_bytes, self._username
        )
        current_password_bytes = credentials.password.encode("utf8")
        is_correct_password = secrets.compare_digest(
            current_password_bytes, self._password
        )
        if not (is_correct_username and is_correct_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Basic"},
            )
        return True
