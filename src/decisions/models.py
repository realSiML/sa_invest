from sqlalchemy import (
    Column,
    Date,
    Enum,
    ForeignKeyConstraint,
    Integer,
    PrimaryKeyConstraint,
    Table,
    Text,
)

from src.models import Base

decision = Table(
    "decision",
    Base.metadata,
    Column("id", Integer),
    Column("support_id", Integer),
    Column(
        "decision_type",
        Enum("EG", "MVK", name="decision_type"),
        comment='Вид решения. Заполняет сотрудник. Источник протокол заседания. По итогам проведения комиссии"',
    ),
    Column(
        "decision_date",
        Date,
        comment="Дата создания решения. Заполняет сотрудник. Источник протокол заседания. По итогам проведения комиссии",
    ),
    Column(
        "protocol_number",
        Text,
        comment="Номер протокола. Заполняет сотрудник. Источник протокол заседания. По итогам проведения комиссии",
    ),
    Column(
        "decision",
        Text,
        comment="Решение. Заполняет сотрудник. Источник протокол заседания. По итогам проведения комиссии",
    ),
    ForeignKeyConstraint(
        ["support_id"], ["support.id"], name="decision_support_id_fkey"
    ),
    PrimaryKeyConstraint("id", name="decision_pkey"),
    comment="Решения о выделении поддержки",
)
