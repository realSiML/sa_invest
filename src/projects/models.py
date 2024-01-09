from sqlalchemy import (
    Column,
    Enum,
    ForeignKeyConstraint,
    Integer,
    Numeric,
    PrimaryKeyConstraint,
    Table,
    Text,
)

from src.models import Base

project = Table(
    "project",
    Base.metadata,
    Column("id", Integer),
    Column("owner_id", Integer),
    Column("address_id", Integer),
    Column("industry_id", Integer),
    Column("name", Text, comment="Название проекта"),
    Column(
        "application_own_amount",
        Numeric,
        comment="Собственная сумма. Заполняет сотрудник. \
            Источник Клиент. По звонку или по заявлению",
    ),
    Column(
        "application_support_amount",
        Numeric,
        comment="Запрашиваемая сумма. Заполняет сотрудник. \
            Источник Клиент. По звонку или по заявлению",
    ),
    Column(
        "work_place_count",
        Integer,
        comment="Количество рабочих мест. Заполняет сотрудник. \
            Источник Клиент. По звонку или по заявлению",
    ),
    Column(
        "nalog_amount",
        Integer,
        comment="Налоги, отчисляемые в бюджет. Заполняет сотрудник. \
            Источник Клиент. По звонку или по заявлению",
    ),
    Column(
        "description",
        Text,
        comment="Описание проекта. Заполняет сотрудник. \
            Источник Клиент. По звонку или по заявлению",
    ),
    Column(
        "state",
        Enum(
            "APPLICANTION_SHORT",
            "APPLICANTION_FULL",
            "DELETED",
            "ENDED",
            "FREEZE",
            "ARCHIVE",
            "PROJECT_IN_COMISSION",
            "PROJECT_ON_SUPPORT",
            name="project_state_type",
        ),
        comment="Состояние проекта",
    ),
    ForeignKeyConstraint(
        ["address_id"], ["address.id"], name="project_address_id_fkey"
    ),
    ForeignKeyConstraint(
        ["industry_id"], ["industry.id"], name="project_industry_id_fkey"
    ),
    ForeignKeyConstraint(
        ["owner_id"], ["owner.id"], name="project_owner_id_fkey"
    ),
    PrimaryKeyConstraint("id", name="project_pkey"),
    comment="Проект",
)
