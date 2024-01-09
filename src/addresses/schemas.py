from pydantic import (
    Field,
    field_validator,
)

from src.schemas import BasePatchSchema, BaseSchema


class AddressBase(BaseSchema):
    district_id: int | None = None
    city_id: int | None = None
    post_code: str = Field(pattern=r"^[0-9]{6}$", description="Почтовый индекс")
    address: str = Field(description="Улица, дом, квартира, офис")

    @field_validator("address")
    def set_title_case(cls, value: str) -> str | None:
        return value.title() if value else None


class AddressCreate(AddressBase):
    pass


class AddressUpdate(AddressBase):
    pass


class Address(AddressBase):
    id: int


class AddressPatch(AddressBase, BasePatchSchema):
    district_id: int | None = None
    city_id: int | None = None
    post_code: str | None = Field(
        default=None, pattern=r"^[0-9]{6}$", description="Почтовый индекс"
    )
    address: str | None = Field(
        default=None, description="Улица, дом, квартира, офис"
    )
