from sqlalchemy import (
    Boolean,
    Column,
    Enum,
    ForeignKeyConstraint,
    Integer,
    MetaData,
    PrimaryKeyConstraint,
    Table,
    Text,
)
from sqlalchemy.orm import declarative_base

from src.constants import DB_NAMING_CONVENTION

Base = declarative_base()

Base.metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)


city = Table(
    "city",
    Base.metadata,
    Column("id", Integer),
    Column("name", Text, comment="Наименование населенного пункта"),
    PrimaryKeyConstraint("id", name="city_pkey"),
    comment="Справочник. Населенные пункты Сахалинской области",
)

district = Table(
    "district",
    Base.metadata,
    Column("id", Integer),
    Column("name", Text, comment="Наименование района"),
    PrimaryKeyConstraint("id", name="district_pkey"),
    comment="Справочник. Районы Сахалинской области",
)

industry = Table(
    "industry",
    Base.metadata,
    Column("id", Integer),
    Column("name", Text, comment="Наименование индустрии"),
    PrimaryKeyConstraint("id", name="industry_pkey"),
    comment="Справочник. Отрасли экономики",
)

support_org = Table(
    "support_org",
    Base.metadata,
    Column("id", Integer),
    Column("name", Text),
    PrimaryKeyConstraint("id", name="support_org_pkey"),
    comment="Справочник. Министерство, ведомство, оказывающее поддержку",
)

support_programm = Table(
    "support_programm",
    Base.metadata,
    Column("id", Integer),
    Column("name", Text, comment="Наименование программы"),
    Column("active", Boolean, comment="Признак активности программы"),
    Column(
        "level_type_code",
        Enum("FEDERAL", "REGION", "MUNICIPAL", name="programm_level_type"),
        comment="Уровень программы",
    ),
    PrimaryKeyConstraint("id", name="support_programm_pkey"),
    comment="Справочник. Федеральные, региональные и муниципальные программы поддержки",
)

business_man = Table(
    "business_man",
    Base.metadata,
    Column("id", Integer),
    Column("address_id", Integer),
    Column("last_name", Text, comment="Фамилия"),
    Column("first_name", Text, comment="Имя"),
    Column("middle_name", Text, comment="Отчество"),
    Column("inn", Text, comment="ИНН"),
    Column("ogrn", Text, comment="ОГРН"),
    ForeignKeyConstraint(
        ["address_id"], ["address.id"], name="business_man_address_id_fkey"
    ),
    PrimaryKeyConstraint("id", name="business_man_pkey"),
    comment="Клиент - ИП или физическое лицо",
)

business_org = Table(
    "business_org",
    Base.metadata,
    Column("id", Integer),
    Column("address_id", Integer),
    Column("name", Text, comment="Полное наименование"),
    Column("name_short", Text, comment="Сокращенное наименование"),
    Column("inn", Text, comment="ИНН"),
    Column("ogrn", Text, comment="ОГРН"),
    ForeignKeyConstraint(
        ["address_id"], ["address.id"], name="business_org_address_id_fkey"
    ),
    PrimaryKeyConstraint("id", name="business_org_pkey"),
    comment="Клиент - юридическое лицо",
)

owner = Table(
    "owner",
    Base.metadata,
    Column("id", Integer),
    Column("business_org_id", Integer),
    Column("business_man_id", Integer),
    ForeignKeyConstraint(
        ["business_man_id"],
        ["business_man.id"],
        name="owner_business_man_id_fkey",
    ),
    ForeignKeyConstraint(
        ["business_org_id"],
        ["business_org.id"],
        name="owner_business_org_id_fkey",
    ),
    PrimaryKeyConstraint("id", name="owner_pkey"),
    comment="Сущность владельца проектом",
)

owner_contact = Table(
    "owner_contact",
    Base.metadata,
    Column("id", Integer),
    Column("owner_id", Integer),
    Column("phone_no", Text, comment="Номер телефона"),
    Column("email", Text, comment="Адрес электронной почты"),
    ForeignKeyConstraint(
        ["owner_id"], ["owner.id"], name="owner_contact_owner_id_fkey"
    ),
    PrimaryKeyConstraint("id", name="owner_contact_pkey"),
    comment="Контакты владельца проектом",
)


user_project = Table(
    "user_project",
    Base.metadata,
    Column("id", Integer),
    Column("user_id", Integer),
    Column("project_id", Integer),
    ForeignKeyConstraint(
        ["project_id"], ["project.id"], name="user_project_project_id_fkey"
    ),
    ForeignKeyConstraint(
        ["user_id"], ["user.id"], name="user_project_user_id_fkey"
    ),
    PrimaryKeyConstraint("id", name="user_project_pkey"),
    comment="Связь пользователей системы с проектами",
)
