from sqlalchemy import (
    Column,
    Enum,
    Integer,
    PrimaryKeyConstraint,
    Table,
    Text,
)

from src.models import Base

user = Table(
    "user",
    Base.metadata,
    Column("id", Integer),
    Column("last_name", Text, comment="Фамилия"),
    Column("first_name", Text, comment="Имя"),
    Column("middle_name", Text, comment="Отчество"),
    Column("email", Text, comment="Адрес электронной почты"),
    Column(
        "role_code",
        Enum(
            "ADMIN",
            "PROJECT_EDITOR",
            "PROJECT_VIEWER",
            "REPORT_EXPORTER_ALL",
            name="role_code_type",
        ),
        comment="Роль пользователя",
    ),
    PrimaryKeyConstraint("id", name="user_pkey"),
    comment="Пользователи системы",
)
