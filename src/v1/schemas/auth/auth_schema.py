from pydantic import BaseModel


class SignupRequestSchema(BaseModel):

    name: str
    email: str
    password: str


class LoginRequestSchema(BaseModel):

    email: str
    password: str


class AuthResponseSchema(BaseModel):

    user_id: int
    name: str
    email: str
    access_token: str