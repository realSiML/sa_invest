from typing import Any

from sqlalchemy import delete, insert, select, update

from src.addresses import models, schemas
from src.database import execute, fetch_all, fetch_one


async def create_address(
    address: schemas.AddressCreate | schemas.AddressUpdate, id: int = None
) -> dict[str, Any]:
    insert_query = (
        insert(models.address)
        .values(address.model_dump())
        .returning(models.address)
    )

    if id is not None:
        insert_query = insert_query.values(id=id)

    db_address = await fetch_one(insert_query)

    return db_address


async def get_addresss() -> list[dict[str, Any]]:
    select_query = select(models.address)

    db_addresss = await fetch_all(select_query)

    return db_addresss


async def get_address_by_id(address_id: int) -> dict[str, Any] | None:
    select_query = select(models.address).where(
        models.address.c.id == address_id
    )

    db_address = await fetch_one(select_query)

    return db_address if db_address is not None else None


async def update_address(
    address: schemas.AddressUpdate | schemas.AddressPatch, id: int
) -> dict[str, Any]:
    update_query = (
        update(models.address)
        .where(models.address.c.id == id)
        .values(address.model_dump(exclude_unset=True))
        .returning(models.address)
    )

    updated_address = await fetch_one(update_query)

    return updated_address


async def update_all_addresss(
    address: schemas.AddressUpdate | schemas.AddressPatch
) -> None:
    update_query = update(models.address).values(
        address.model_dump(exclude_unset=True)
    )

    await execute(update_query)


async def delete_address(address_id: int) -> None:
    delete_query = delete(models.address).where(
        models.address.c.id == address_id
    )

    await execute(delete_query)


async def delete_all_addresss() -> None:
    delete_query = delete(models.address)

    await execute(delete_query)
