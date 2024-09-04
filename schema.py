from pydantic import BaseModel, field_validator
from flask import request

from models import Session, User, Advertisement


class UpdateAdv(BaseModel):
    title: str | None = None
    description: str | None = None
    owner: int

    # @field_validator('owner')
    # @classmethod
    # def check_owner(cls, value):
    #     session = Session()
    #     adv_owner = session.get(Advertisement, request.root_path).owner
    #     session.close()
    #     if adv_owner != value:
    #         raise ValueError("Недостаточно прав")
    #
    #     return value


class CreateAdv(BaseModel):
    title: str
    description: str
    owner: int

    @field_validator("owner")
    @classmethod
    def check_owner(cls, value):
        session = Session()
        user = session.get(User, value)
        session.close()
        if user is None:
            raise ValueError("Пользователь должен быть зарегистрирован")

        return value


class UserBase(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None

    @field_validator("password")
    @classmethod
    def check_password(cls, value):
        if len(value) < 8:
            raise ValueError("Пароль должен быть не менее 8 символов")
        return value


class UpdateUser(UserBase):
    name: str | None = None
    email: str | None = None
    password: str | None = None


class CreateUser(UserBase):
    name: str
    email: str
    password: str
