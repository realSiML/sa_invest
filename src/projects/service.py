from typing import Any

from sqlalchemy import delete, insert, select, update

from src.database import execute, fetch_all, fetch_one
from src.projects import models, schemas


async def create_project(
    project: schemas.ProjectCreate | schemas.ProjectUpdate, id: int = None
) -> dict[str, Any]:
    insert_query = (
        insert(models.project)
        .values(project.model_dump())
        .returning(models.project)
    )

    if id is not None:
        insert_query = insert_query.values(id=id)

    db_project = await fetch_one(insert_query)

    return db_project


async def get_projects() -> list[dict[str, Any]]:
    select_query = select(models.project)

    db_projects = await fetch_all(select_query)

    return db_projects


async def get_project_by_id(project_id: int) -> dict[str, Any] | None:
    select_query = select(models.project).where(
        models.project.c.id == project_id
    )

    db_project = await fetch_one(select_query)

    return db_project if db_project is not None else None


async def update_project(
    project: schemas.ProjectUpdate | schemas.ProjectPatch, id: int
) -> dict[str, Any]:
    update_query = (
        update(models.project)
        .where(models.project.c.id == id)
        .values(project.model_dump(exclude_unset=True))
        .returning(models.project)
    )

    updated_project = await fetch_one(update_query)

    return updated_project


async def update_all_projects(
    project: schemas.ProjectUpdate | schemas.ProjectPatch
) -> None:
    update_query = update(models.project).values(
        project.model_dump(exclude_unset=True)
    )

    await execute(update_query)


async def delete_project(project_id: int) -> None:
    delete_query = delete(models.project).where(
        models.project.c.id == project_id
    )

    await execute(delete_query)


async def delete_all_projects() -> None:
    delete_query = delete(models.project)

    await execute(delete_query)
