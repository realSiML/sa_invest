from typing import Literal

from pydantic import BaseModel, Field, field_validator

from src.schemas import BasePatchSchema

ProjectStateType = Literal[
    "APPLICANTION_SHORT",
    "APPLICANTION_FULL",
    "DELETED",
    "ENDED",
    "FREEZE",
    "ARCHIVE",
    "PROJECT_IN_COMISSION",
    "PROJECT_ON_SUPPORT",
]


class ProjectBase(BaseModel):
    user_id: int | None = None
    owner_id: int | None = None
    address_id: int | None = None
    industry_id: int | None = None
    name: str = Field(description="Название проекта")
    application_own_amount: float = Field(
        ge=0,
        description="Собственная сумма. Заполняет сотрудник. \
            Источник Клиент. По звонку или по заявлению",
    )
    application_support_amount: float = Field(
        ge=0,
        description="Запрашиваемая сумма. Заполняет сотрудник. \
            Источник Клиент. По звонку или по заявлению",
    )
    work_place_count: int = Field(
        ge=0,
        description="Количество рабочих мест. Заполняет сотрудник. \
            Источник Клиент. По звонку или по заявлению",
    )
    nalog_amount: int = Field(
        ge=0,
        description="Налоги, отчисляемые в бюджет. Заполняет сотрудник. \
            Источник Клиент. По звонку или по заявлению",
    )
    description: str | None = Field(
        default=None,
        description="Описание проекта. Заполняет сотрудник. \
            Источник Клиент. По звонку или по заявлению",
    )
    state: ProjectStateType = Field(description="Состояние проекта")

    @field_validator("name")
    def set_title_case(cls, value: str) -> str | None:
        return value.title() if value else None

    @field_validator("description")
    def format_str(cls, value: str | None) -> str | None:
        return value[0].upper() + value[1:].lower() if value else None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    pass


class Project(ProjectBase):
    id: int


class ProjectPatch(ProjectBase, BasePatchSchema):
    user_id: int | None = None
    owner_id: int | None = None
    address_id: int | None = None
    industry_id: int | None = None
    name: str = Field(default=None, description="Название проекта")
    application_own_amount: float = Field(
        ge=0,
        default=None,
        description="Собственная сумма. Заполняет сотрудник. \
            Источник Клиент. По звонку или по заявлению",
    )
    application_support_amount: float = Field(
        ge=0,
        default=None,
        description="Запрашиваемая сумма. Заполняет сотрудник. \
            Источник Клиент. По звонку или по заявлению",
    )
    work_place_count: int = Field(
        ge=0,
        default=None,
        description="Количество рабочих мест. Заполняет сотрудник. \
            Источник Клиент. По звонку или по заявлению",
    )
    nalog_amount: int = Field(
        ge=0,
        default=None,
        description="Налоги, отчисляемые в бюджет. Заполняет сотрудник. \
            Источник Клиент. По звонку или по заявлению",
    )
    description: str | None = Field(
        default=None,
        description="Описание проекта. Заполняет сотрудник. \
            Источник Клиент. По звонку или по заявлению",
    )
    state: ProjectStateType = Field(
        default=None, description="Состояние проекта"
    )
