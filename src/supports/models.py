from sqlalchemy import (
    Column,
    Date,
    Enum,
    ForeignKeyConstraint,
    Integer,
    Numeric,
    PrimaryKeyConstraint,
    Table,
    Text,
    UniqueConstraint,
)

from src.models import Base

support = Table(
    "support",
    Base.metadata,
    Column("id", Integer),
    Column(
        "project_id",
        Integer,
        comment="ID проекта к которому относится поддержка",
    ),
    Column(
        "support_programm_id",
        Integer,
        comment="ID государственной программы, по которой выделяется поддержка",
    ),
    Column(
        "support_org_id",
        Integer,
        comment="ID государственного органа, выделяющего поддержку",
    ),
    Column("date_start", Date, comment="Дата начала выделения поддержки"),
    Column("date_end", Date, comment="Дата окончания выделения поддержки"),
    Column(
        "type_code",
        Enum(
            "FINANCE", "CREDIT", "EARTH", "EQUIP", "TECH", name="support_type"
        ),
        comment="Вид поддержки",
    ),
    Column("amount", Numeric, comment="Размер поддержки"),
    Column(
        "unit",
        Enum(
            "RUB",
            "PIECES",
            "METERS",
            "METERS_CUBIC",
            "METERS_SQUARE",
            "HECTARES",
            name="unit_type",
        ),
    ),
    Column("desc", Text, comment="Описание"),
    ForeignKeyConstraint(
        ["project_id"], ["project.id"], name="support_project_id_fkey"
    ),
    ForeignKeyConstraint(
        ["support_org_id"],
        ["support_org.id"],
        name="support_support_org_id_fkey",
    ),
    ForeignKeyConstraint(
        ["support_programm_id"],
        ["support_programm.id"],
        name="support_support_programm_id_fkey",
    ),
    PrimaryKeyConstraint("id", name="support_pkey"),
    UniqueConstraint("project_id", name="support_project_id_key"),
    UniqueConstraint("support_org_id", name="support_support_org_id_key"),
    UniqueConstraint(
        "support_programm_id", name="support_support_programm_id_key"
    ),
    comment="Поддержка по проекту",
)
