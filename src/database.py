from typing import Any

from sqlalchemy import CursorResult, Delete, Insert, Select, Update
from sqlalchemy.ext.asyncio import create_async_engine

from src.config import settings

engine = create_async_engine(settings.DATABASE_URL.unicode_string(), echo=True)


async def fetch_one(
    query: Select | Insert | Update | Delete
) -> dict[str, Any] | None:
    async with engine.begin() as conn:
        cursor: CursorResult = await conn.execute(query)
        return cursor.first()._asdict() if cursor.rowcount > 0 else None


async def fetch_all(
    query: Select | Insert | Update | Delete
) -> list[dict[str, Any]]:
    async with engine.begin() as conn:
        cursor: CursorResult = await conn.execute(query)
        return [r._asdict() for r in cursor.all()]


async def execute(query: Insert | Update | Delete) -> None:
    async with engine.begin() as conn:
        await conn.execute(query)
