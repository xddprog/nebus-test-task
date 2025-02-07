from fastapi import HTTPException


class UserAlreadyRegistered(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="User already registered")


class UserNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="User not found")