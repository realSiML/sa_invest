from datetime import date
from typing import Literal

from pydantic import (
    Field,
    field_validator,
)

from src.schemas import BasePatchSchema, BaseSchema

DecisionType = Literal["EG", "MVK"]


class DecisionBase(BaseSchema):
    support_id: int | None = None
    decision_type: DecisionType = Field(
        description="Вид решения. Заполняет сотрудник. Источник протокол заседания. По итогам проведения комиссии"
    )
    decision_date: date = Field(
        description="Дата создания решения. Заполняет сотрудник. Источник протокол заседания. По итогам проведения комиссии"
    )
    protocol_number: str = Field(
        description="Номер протокола. Заполняет сотрудник. Источник протокол заседания. По итогам проведения комиссии"
    )
    decision: str = Field(
        description="Решение. Заполняет сотрудник. Источник протокол заседания. По итогам проведения комиссии"
    )

    @field_validator("protocol_number")
    def set_upper_case(cls, value: str) -> str | None:
        return value.upper() if value != "" else None

    @field_validator("decision")
    def format_str(cls, value: str) -> str | None:
        return value[0].upper() + value[1:].lower() if value else None


class DecisionCreate(DecisionBase):
    pass


class DecisionUpdate(DecisionBase):
    pass


class Decision(DecisionBase):
    id: int


class DecisionPatch(DecisionBase, BasePatchSchema):
    support_id: int | None = None
    decision_type: DecisionType | None = Field(
        default=None,
        description="Вид решения. Заполняет сотрудник. Источник протокол заседания. По итогам проведения комиссии",
    )
    decision_date: date | None = Field(
        default=None,
        description="Дата создания решения. Заполняет сотрудник. Источник протокол заседания. По итогам проведения комиссии",
    )
    protocol_number: str | None = Field(
        default=None,
        description="Номер протокола. Заполняет сотрудник. Источник протокол заседания. По итогам проведения комиссии",
    )
    decision: str | None = Field(
        default=None,
        description="Решение. Заполняет сотрудник. Источник протокол заседания. По итогам проведения комиссии",
    )
