from fastapi import APIRouter, HTTPException, Response, status

from src.constants import PathParamId
from src.decisions import service
from src.decisions.schemas import (
    Decision,
    DecisionCreate,
    DecisionPatch,
    DecisionUpdate,
)

router = APIRouter(prefix="/decisions", tags=["Решения"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Создать новое решение",
)
async def create_decision(decision: DecisionCreate):
    new_decision = await service.create_decision(decision)

    headers = {"Location": f"{router.prefix}/{new_decision['id']}"}
    return Response(status_code=status.HTTP_201_CREATED, headers=headers)


@router.get(
    "/",
    response_model=list[Decision],
    status_code=status.HTTP_200_OK,
    summary="Получить список решений",
)
async def get_decisions(response: Response):
    db_decisions = await service.get_decisions()

    response.headers["Content-Location"] = router.prefix
    return db_decisions


@router.get(
    "/{decision_id}",
    response_model=Decision,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": None},
    },
    summary="Получить решение по id",
)
async def get_decision_by_id(decision_id: PathParamId, response: Response):
    db_decision = await service.get_decision_by_id(decision_id)

    if db_decision is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    response.headers["Content-Location"] = f"{router.prefix}/{decision_id}"
    return db_decision


@router.put(
    "/",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Заменить данные всех решений",
)
async def update_all_decisions(decision: DecisionUpdate):
    db_decisions = await service.get_decisions()

    if db_decisions:
        await service.update_all_decisions(decision)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# SELECT setval('decision_id_seq', (SELECT COALESCE(MAX(id), 0) FROM "decision"));
@router.put(
    "/{decision_id}",
    response_model=Decision,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_201_CREATED: {"model": None},
        status.HTTP_204_NO_CONTENT: {"model": None},
    },
    summary="Заменить данные решения или создать новое",
)
async def update_decision(
    decision_id: PathParamId, decision: DecisionUpdate, response: Response
):
    db_decision = await service.get_decision_by_id(decision_id)

    # Если нет, создаем нового с таким id
    if db_decision is None:
        await service.create_decision(decision, decision_id)

        headers = {"Location": f"{router.prefix}/{decision_id}"}
        return Response(status_code=status.HTTP_201_CREATED, headers=headers)
    else:
        response.headers["Content-Location"] = f"{router.prefix}/{decision_id}"

    # Если нет изменений, возвращем 204
    put_fields = decision.model_dump()
    if all(put_fields[key] == db_decision[key] for key in put_fields):
        return Response(
            status_code=status.HTTP_204_NO_CONTENT, headers=response.headers
        )

    # Если есть, обновляем
    updated_decision = await service.update_decision(decision, decision_id)
    return updated_decision


@router.delete(
    "/",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить все решения",
)
async def delete_all_decisions():
    await service.delete_all_decisions()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
    "/{decision_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": None},
    },
    summary="Удалить решение",
)
async def delete_decision(decision_id: PathParamId):
    db_decision = await service.get_decision_by_id(decision_id)

    if db_decision is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    await service.delete_decision(decision_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch(
    "/",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Изменить данные всех решений",
)
async def patch_all_decisions(decision: DecisionPatch):
    db_decisions = await service.get_decisions()

    if db_decisions:
        await service.update_all_decisions(decision)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch(
    "/{decision_id}",
    response_model=Decision,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_204_NO_CONTENT: {"model": None},
        status.HTTP_404_NOT_FOUND: {"model": None},
    },
    summary="Изменить данные решения",
)
async def patch_decision(
    decision_id: PathParamId, decision: DecisionPatch, response: Response
):
    db_decision = await service.get_decision_by_id(decision_id)

    # Если нет, 404
    if db_decision is None:
        raise HTTPException(status_code=404)
    else:
        response.headers["Content-Location"] = f"{router.prefix}/{decision_id}"

    # Если нет изменений, возвращем 204
    patch_fields = decision.model_dump(exclude_unset=True)
    if all(patch_fields[key] == db_decision[key] for key in patch_fields):
        return Response(
            status_code=status.HTTP_204_NO_CONTENT, headers=response.headers
        )

    # Если есть, обновляем
    db_decision = await service.update_decision(decision, decision_id)

    return db_decision
