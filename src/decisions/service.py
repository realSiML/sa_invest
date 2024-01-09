from typing import Any

from sqlalchemy import delete, insert, select, update

from src.database import execute, fetch_all, fetch_one
from src.decisions import models, schemas


async def create_decision(
    decision: schemas.DecisionCreate | schemas.DecisionUpdate, id: int = None
) -> dict[str, Any]:
    insert_query = (
        insert(models.decision)
        .values(decision.model_dump())
        .returning(models.decision)
    )

    if id is not None:
        insert_query = insert_query.values(id=id)

    db_decision = await fetch_one(insert_query)

    return db_decision


async def get_decisions() -> list[dict[str, Any]]:
    select_query = select(models.decision)

    db_decisions = await fetch_all(select_query)

    return db_decisions


async def get_decision_by_id(decision_id: int) -> dict[str, Any] | None:
    select_query = select(models.decision).where(
        models.decision.c.id == decision_id
    )

    db_decision = await fetch_one(select_query)

    return db_decision if db_decision is not None else None


async def update_decision(
    decision: schemas.DecisionUpdate | schemas.DecisionPatch, id: int
) -> dict[str, Any]:
    update_query = (
        update(models.decision)
        .where(models.decision.c.id == id)
        .values(decision.model_dump(exclude_unset=True))
        .returning(models.decision)
    )

    updated_decision = await fetch_one(update_query)

    return updated_decision


async def update_all_decisions(
    decision: schemas.DecisionUpdate | schemas.DecisionPatch
) -> None:
    update_query = update(models.decision).values(
        decision.model_dump(exclude_unset=True)
    )

    await execute(update_query)


async def delete_decision(decision_id: int) -> None:
    delete_query = delete(models.decision).where(
        models.decision.c.id == decision_id
    )

    await execute(delete_query)


async def delete_all_decisions() -> None:
    delete_query = delete(models.decision)

    await execute(delete_query)
