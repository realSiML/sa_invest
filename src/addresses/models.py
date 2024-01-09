from sqlalchemy import (
    Column,
    ForeignKeyConstraint,
    Integer,
    PrimaryKeyConstraint,
    Table,
    Text,
)

from src.models import Base

address = Table(
    "address",
    Base.metadata,
    Column("id", Integer),
    Column("district_id", Integer),
    Column("city_id", Integer),
    Column("post_code", Text, comment="Почтовый индекс"),
    Column("address", Text, comment="Улица, дом, квартира, офис"),
    ForeignKeyConstraint(["city_id"], ["city.id"], name="address_city_id_fkey"),
    ForeignKeyConstraint(
        ["district_id"], ["district.id"], name="address_district_id_fkey"
    ),
    PrimaryKeyConstraint("id", name="address_pkey"),
    comment="Адреса",
)
