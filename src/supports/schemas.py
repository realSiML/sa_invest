from datetime import date
from typing import Literal

from pydantic import Field, field_validator

from src.schemas import BasePatchSchema, BaseSchema

SupportType = Literal["FINANCE", "CREDIT", "EARTH", "EQUIP", "TECH"]


UnitType = Literal[
    "RUB", "PIECES", "METERS", "METERS_CUBIC", "METERS_SQUARE", "HECTARES"
]


class SupportBase(BaseSchema):
    project_id: int | None = None
    support_programm_id: int | None = None
    support_org_id: int | None = None
    date_start: date = Field(description="Дата начала выделения поддержки")
    date_end: date | None = Field(
        default=None, description="Дата окончания выделения поддержки"
    )
    type_code: SupportType = Field(description="Вид поддержки")
    amount: float = Field(description="Размер поддержки")
    unit: UnitType = Field(description="Единицы измерения")
    desc: str | None = Field(default=None, description="Описание")

    @field_validator("desc")
    def remove_empty_str(cls, value: str | None) -> str | None:
        return value if value != "" else None

    @field_validator("desc")
    def format_str(cls, value: str | None) -> str | None:
        return value[0].upper() + value[1:].lower() if value else None


class SupportCreate(SupportBase):
    pass


class SupportUpdate(SupportBase):
    pass


class Support(SupportBase):
    id: int

    # FIXME: https://github.com/zhanymkanov/fastapi-best-practices#3-use-dependencies-for-data-validation-vs-db
    # @model_validator(mode="after")
    # def validate_date_end(self):
    #     if self.date_end is not None and self.date_end < self.date_start:
    #         raise ValueError(
    #             "Дата окончания выделения поддержки должна быть не раньше даты начала"
    #         )

    #     return self

    # @model_validator(mode="after")
    # def validate_type_with_unit(self):
    #     try:
    #         match self.type_code:
    #             case "FINANCE" | "CREDIT":
    #                 if self.unit != "RUB":
    #                     raise ValueError
    #             case "EQUIP" | "TECH":
    #                 if self.unit != "PIECES":
    #                     raise ValueError
    #             case _:
    #                 if self.unit in ("RUB", "PIECES"):
    #                     raise ValueError
    #     except ValueError:
    #         print(self)
    #         raise ValueError(
    #             f"Единицы измерения ({self.unit}) \
    #                 не соответствуют виду поддержки ({self.type_code})"
    #         )
    #     else:
    #         return self


class SupportPatch(SupportBase, BasePatchSchema):
    project_id: int | None = None
    support_programm_id: int | None = None
    support_org_id: int | None = None
    date_start: date | None = Field(
        default=None, description="Дата начала выделения поддержки"
    )
    date_end: date | None = Field(
        default=None, description="Дата окончания выделения поддержки"
    )
    type_code: SupportType | None = Field(
        default=None, description="Вид поддержки"
    )
    amount: float | None = Field(default=None, description="Размер поддержки")
    unit: UnitType | None = Field(default=None, description="Единицы измерения")
    desc: str | None = Field(default=None, description="Описание")
