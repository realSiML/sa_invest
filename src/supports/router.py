from fastapi import APIRouter, HTTPException, Response, status

from src.constants import PathParamId
from src.supports import service
from src.supports.schemas import (
    Support,
    SupportCreate,
    SupportPatch,
    SupportUpdate,
)

router = APIRouter(prefix="/supports", tags=["Поддержки"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Создать новую поддержку",
)
async def create_support(support: SupportCreate):
    new_support = await service.create_support(support)

    headers = {"Location": f"{router.prefix}/{new_support['id']}"}
    return Response(status_code=status.HTTP_201_CREATED, headers=headers)


@router.get(
    "/",
    response_model=list[Support],
    status_code=status.HTTP_200_OK,
    summary="Получить список поддержки",
)
async def get_supports(response: Response):
    db_supports = await service.get_supports()

    response.headers["Content-Location"] = router.prefix
    return db_supports


@router.get(
    "/{support_id}",
    response_model=Support,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": None},
    },
    summary="Получить поддержку по id",
)
async def get_support_by_id(support_id: PathParamId, response: Response):
    db_support = await service.get_support_by_id(support_id)

    if db_support is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    response.headers["Content-Location"] = f"{router.prefix}/{support_id}"
    return db_support


@router.put(
    "/",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Заменить данные всех поддержек",
)
async def update_all_supports(support: SupportUpdate):
    db_supports = await service.get_supports()

    if db_supports:
        await service.update_all_supports(support)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# SELECT setval('support_id_seq', (SELECT COALESCE(MAX(id), 0) FROM "support"));
@router.put(
    "/{support_id}",
    response_model=Support,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_201_CREATED: {"model": None},
        status.HTTP_204_NO_CONTENT: {"model": None},
    },
    summary="Заменить данные поддержки или создать новую",
)
async def update_support(
    support_id: PathParamId, support: SupportUpdate, response: Response
):
    db_support = await service.get_support_by_id(support_id)

    # Если нет, создаем нового с таким id
    if db_support is None:
        await service.create_support(support, support_id)

        headers = {"Location": f"{router.prefix}/{support_id}"}
        return Response(status_code=status.HTTP_201_CREATED, headers=headers)
    else:
        response.headers["Content-Location"] = f"{router.prefix}/{support_id}"

    # Если нет изменений, возвращем 204
    put_fields = support.model_dump()
    if all(put_fields[key] == db_support[key] for key in put_fields):
        return Response(
            status_code=status.HTTP_204_NO_CONTENT, headers=response.headers
        )

    # Если есть, обновляем
    updated_support = await service.update_support(support, support_id)
    return updated_support


@router.delete(
    "/",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить все поддержки",
)
async def delete_all_supports():
    await service.delete_all_supports()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
    "/{support_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": None},
    },
    summary="Удалить поддержку",
)
async def delete_support(support_id: PathParamId):
    db_support = await service.get_support_by_id(support_id)

    if db_support is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    await service.delete_support(support_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch(
    "/",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Изменить данные всех поддержек",
)
async def patch_all_supports(support: SupportPatch):
    db_supports = await service.get_supports()

    if db_supports:
        await service.update_all_supports(support)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch(
    "/{support_id}",
    response_model=Support,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_204_NO_CONTENT: {"model": None},
        status.HTTP_404_NOT_FOUND: {"model": None},
    },
    summary="Изменить данные поддержки",
)
async def patch_support(
    support_id: PathParamId, support: SupportPatch, response: Response
):
    db_support = await service.get_support_by_id(support_id)

    # Если нет, 404
    if db_support is None:
        raise HTTPException(status_code=404)
    else:
        response.headers["Content-Location"] = f"{router.prefix}/{support_id}"

    # Если нет изменений, возвращем 204
    patch_fields = support.model_dump(exclude_unset=True)
    if all(patch_fields[key] == db_support[key] for key in patch_fields):
        return Response(
            status_code=status.HTTP_204_NO_CONTENT, headers=response.headers
        )

    # Если есть, обновляем
    db_support = await service.update_support(support, support_id)

    return db_support
