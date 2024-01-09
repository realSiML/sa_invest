from fastapi import APIRouter, HTTPException, Response, status

from src.constants import PathParamId
from src.users import service
from src.users.schemas import User, UserCreate, UserPatch, UserUpdate

router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Создать нового пользователя",
)
async def create_user(user: UserCreate):
    new_user = await service.create_user(user)

    headers = {"Location": f"{router.prefix}/{new_user['id']}"}
    return Response(status_code=status.HTTP_201_CREATED, headers=headers)


@router.get(
    "/",
    response_model=list[User],
    status_code=status.HTTP_200_OK,
    summary="Получить список пользователей",
)
async def get_users(response: Response):
    db_users = await service.get_users()

    response.headers["Content-Location"] = router.prefix
    return db_users


@router.get(
    "/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": None},
    },
    summary="Получить пользователя по id",
)
async def get_user_by_id(user_id: PathParamId, response: Response):
    db_user = await service.get_user_by_id(user_id)

    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    response.headers["Content-Location"] = f"{router.prefix}/{user_id}"
    return db_user


@router.put(
    "/",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Заменить данные всех пользователей",
)
async def update_all_users(user: UserUpdate):
    db_users = await service.get_users()

    if db_users:
        await service.update_all_users(user)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# SELECT setval('user_id_seq', (SELECT COALESCE(MAX(id), 0) FROM "user"));
@router.put(
    "/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_201_CREATED: {"model": None},
        status.HTTP_204_NO_CONTENT: {"model": None},
    },
    summary="Заменить данные пользователя или создать нового",
)
async def update_user(
    user_id: PathParamId, user: UserUpdate, response: Response
):
    db_user = await service.get_user_by_id(user_id)

    # Если нет, создаем нового с таким id
    if db_user is None:
        await service.create_user(user, user_id)

        headers = {"Location": f"{router.prefix}/{user_id}"}
        return Response(status_code=status.HTTP_201_CREATED, headers=headers)
    else:
        response.headers["Content-Location"] = f"{router.prefix}/{user_id}"

    # Если нет изменений, возвращем 204
    put_fields = user.model_dump()
    if all(put_fields[key] == db_user[key] for key in put_fields):
        return Response(
            status_code=status.HTTP_204_NO_CONTENT, headers=response.headers
        )

    # Если есть, обновляем
    updated_user = await service.update_user(user, user_id)
    return updated_user


@router.delete(
    "/",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить всех пользователей",
)
async def delete_all_users():
    await service.delete_all_users()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
    "/{user_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": None},
    },
    summary="Удалить пользователя",
)
async def delete_user(user_id: PathParamId):
    db_user = await service.get_user_by_id(user_id)

    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    await service.delete_user(user_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch(
    "/",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Изменить данные всех пользователей",
)
async def patch_all_users(user: UserPatch):
    db_users = await service.get_users()

    if db_users:
        await service.update_all_users(user)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch(
    "/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_204_NO_CONTENT: {"model": None},
        status.HTTP_404_NOT_FOUND: {"model": None},
    },
    summary="Изменить данные пользователя",
)
async def patch_user(user_id: PathParamId, user: UserPatch, response: Response):
    db_user = await service.get_user_by_id(user_id)

    # Если нет, 404
    if db_user is None:
        raise HTTPException(status_code=404)
    else:
        response.headers["Content-Location"] = f"{router.prefix}/{user_id}"

    # Если нет изменений, возвращем 204
    patch_fields = user.model_dump(exclude_unset=True)
    if all(patch_fields[key] == db_user[key] for key in patch_fields):
        return Response(
            status_code=status.HTTP_204_NO_CONTENT, headers=response.headers
        )

    # Если есть, обновляем
    db_user = await service.update_user(user, user_id)

    return db_user
