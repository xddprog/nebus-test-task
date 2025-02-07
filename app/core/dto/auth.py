from pydantic import BaseModel


class AuthUserModel(BaseModel):
    email: str
    password: str


class GetTGTokenModel(BaseModel):
    secret_key: str