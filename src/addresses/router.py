from fastapi import APIRouter, HTTPException, Response, status

from src.addresses import service
from src.addresses.schemas import (
    Address,
    AddressCreate,
    AddressPatch,
    AddressUpdate,
)
from src.constants import PathParamId

router = APIRouter(prefix="/addresses", tags=["Адреса"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Создать новый адрес",
)
async def create_address(address: AddressCreate):
    new_address = await service.create_address(address)

    headers = {"Location": f"{router.prefix}/{new_address['id']}"}
    return Response(status_code=status.HTTP_201_CREATED, headers=headers)


@router.get(
    "/",
    response_model=list[Address],
    status_code=status.HTTP_200_OK,
    summary="Получить список адресов",
)
async def get_addresss(response: Response):
    db_addresss = await service.get_addresss()

    response.headers["Content-Location"] = router.prefix
    return db_addresss


@router.get(
    "/{address_id}",
    response_model=Address,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": None},
    },
    summary="Получить адрес по id",
)
async def get_address_by_id(address_id: PathParamId, response: Response):
    db_address = await service.get_address_by_id(address_id)

    if db_address is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    response.headers["Content-Location"] = f"{router.prefix}/{address_id}"
    return db_address


@router.put(
    "/",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Заменить данные всех адресов",
)
async def update_all_addresss(address: AddressUpdate):
    db_addresss = await service.get_addresss()

    if db_addresss:
        await service.update_all_addresss(address)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# SELECT setval('address_id_seq', (SELECT COALESCE(MAX(id), 0) FROM "address"));
@router.put(
    "/{address_id}",
    response_model=Address,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_201_CREATED: {"model": None},
        status.HTTP_204_NO_CONTENT: {"model": None},
    },
    summary="Заменить данные адреса или создать новый",
)
async def update_address(
    address_id: PathParamId, address: AddressUpdate, response: Response
):
    db_address = await service.get_address_by_id(address_id)

    # Если нет, создаем нового с таким id
    if db_address is None:
        await service.create_address(address, address_id)

        headers = {"Location": f"{router.prefix}/{address_id}"}
        return Response(status_code=status.HTTP_201_CREATED, headers=headers)
    else:
        response.headers["Content-Location"] = f"{router.prefix}/{address_id}"

    # Если нет изменений, возвращем 204
    put_fields = address.model_dump()
    if all(put_fields[key] == db_address[key] for key in put_fields):
        return Response(
            status_code=status.HTTP_204_NO_CONTENT, headers=response.headers
        )

    # Если есть, обновляем
    updated_address = await service.update_address(address, address_id)
    return updated_address


@router.delete(
    "/",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить все адреса",
)
async def delete_all_addresss():
    await service.delete_all_addresss()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
    "/{address_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": None},
    },
    summary="Удалить адрес",
)
async def delete_address(address_id: PathParamId):
    db_address = await service.get_address_by_id(address_id)

    if db_address is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    await service.delete_address(address_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch(
    "/",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Изменить данные всех адресов",
)
async def patch_all_addresss(address: AddressPatch):
    db_addresss = await service.get_addresss()

    if db_addresss:
        await service.update_all_addresss(address)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch(
    "/{address_id}",
    response_model=Address,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_204_NO_CONTENT: {"model": None},
        status.HTTP_404_NOT_FOUND: {"model": None},
    },
    summary="Изменить данные адреса",
)
async def patch_address(
    address_id: PathParamId, address: AddressPatch, response: Response
):
    db_address = await service.get_address_by_id(address_id)

    # Если нет, 404
    if db_address is None:
        raise HTTPException(status_code=404)
    else:
        response.headers["Content-Location"] = f"{router.prefix}/{address_id}"

    # Если нет изменений, возвращем 204
    patch_fields = address.model_dump(exclude_unset=True)
    if all(patch_fields[key] == db_address[key] for key in patch_fields):
        return Response(
            status_code=status.HTTP_204_NO_CONTENT, headers=response.headers
        )

    # Если есть, обновляем
    db_address = await service.update_address(address, address_id)

    return db_address
