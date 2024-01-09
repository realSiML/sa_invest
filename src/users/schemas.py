from typing import Literal

from pydantic import (
    EmailStr,
    Field,
    field_validator,
)

from src.schemas import BasePatchSchema, BaseSchema

RoleCode = Literal[
    "ADMIN", "PROJECT_EDITOR", "PROJECT_VIEWER", "REPORT_EXPORTER_ALL"
]


class UserBase(BaseSchema):
    last_name: str = Field(description="Фамилия")
    first_name: str = Field(description="Имя")
    middle_name: str | None = Field(default=None, description="Отчество")
    email: EmailStr = Field(description="Адрес электронной почты")
    role_code: RoleCode = Field(description="Роль пользователя")

    @field_validator("middle_name")
    def remove_empty_str(cls, value: str) -> str | None:
        return value if value != "" else None

    @field_validator("last_name", "first_name", "middle_name")
    def set_title_case(cls, value: str) -> str | None:
        return value.title() if value else None

    @field_validator("email")
    def set_lower_case(cls, value: str) -> str | None:
        return value.lower() if value else None


class User(UserBase):
    id: int


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class UserPatch(UserBase, BasePatchSchema):
    last_name: str | None = Field(default=None, description="Фамилия")
    first_name: str | None = Field(default=None, description="Имя")
    middle_name: str | None = Field(default=None, description="Отчество")
    email: EmailStr | None = Field(
        default=None, description="Адрес электронной почты"
    )
    role_code: RoleCode | None = Field(
        default=None, description="Роль пользователя"
    )
