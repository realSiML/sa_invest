from typing import Any

from sqlalchemy import delete, insert, select, update

from src.database import execute, fetch_all, fetch_one
from src.users import models, schemas


async def create_user(
    user: schemas.UserCreate | schemas.UserUpdate, id: int = None
) -> dict[str, Any]:
    insert_query = (
        insert(models.user).values(user.model_dump()).returning(models.user)
    )

    if id is not None:
        insert_query = insert_query.values(id=id)

    db_user = await fetch_one(insert_query)

    return db_user


async def get_users() -> list[dict[str, Any]]:
    select_query = select(models.user)

    db_users = await fetch_all(select_query)

    return db_users


async def get_user_by_id(user_id: int) -> dict[str, Any] | None:
    select_query = select(models.user).where(models.user.c.id == user_id)

    db_user = await fetch_one(select_query)

    return db_user if db_user is not None else None


async def update_user(
    user: schemas.UserUpdate | schemas.UserPatch, id: int
) -> dict[str, Any]:
    update_query = (
        update(models.user)
        .where(models.user.c.id == id)
        .values(user.model_dump(exclude_unset=True))
        .returning(models.user)
    )

    updated_user = await fetch_one(update_query)

    return updated_user


async def update_all_users(
    user: schemas.UserUpdate | schemas.UserPatch
) -> None:
    update_query = update(models.user).values(
        user.model_dump(exclude_unset=True)
    )

    await execute(update_query)


async def delete_user(user_id: int) -> None:
    delete_query = delete(models.user).where(models.user.c.id == user_id)

    await execute(delete_query)


async def delete_all_users() -> None:
    delete_query = delete(models.user)

    await execute(delete_query)
