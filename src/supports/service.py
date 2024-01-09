from typing import Any

from sqlalchemy import delete, insert, select, update

from src.database import execute, fetch_all, fetch_one
from src.supports import models, schemas


async def create_support(
    support: schemas.SupportCreate | schemas.SupportUpdate, id: int = None
) -> dict[str, Any]:
    insert_query = (
        insert(models.support)
        .values(support.model_dump())
        .returning(models.support)
    )

    if id is not None:
        insert_query = insert_query.values(id=id)

    db_support = await fetch_one(insert_query)

    return db_support


async def get_supports() -> list[dict[str, Any]]:
    select_query = select(models.support)

    db_supports = await fetch_all(select_query)

    return db_supports


async def get_support_by_id(support_id: int) -> dict[str, Any] | None:
    select_query = select(models.support).where(
        models.support.c.id == support_id
    )

    db_support = await fetch_one(select_query)

    return db_support if db_support is not None else None


async def update_support(
    support: schemas.SupportUpdate | schemas.SupportPatch, id: int
) -> dict[str, Any]:
    update_query = (
        update(models.support)
        .where(models.support.c.id == id)
        .values(support.model_dump(exclude_unset=True))
        .returning(models.support)
    )

    updated_support = await fetch_one(update_query)

    return updated_support


async def update_all_supports(
    support: schemas.SupportUpdate | schemas.SupportPatch
) -> None:
    update_query = update(models.support).values(
        support.model_dump(exclude_unset=True)
    )

    await execute(update_query)


async def delete_support(support_id: int) -> None:
    delete_query = delete(models.support).where(
        models.support.c.id == support_id
    )

    await execute(delete_query)


async def delete_all_supports() -> None:
    delete_query = delete(models.support)

    await execute(delete_query)
