from fastapi import APIRouter, HTTPException, Response, status

from src.constants import PathParamId
from src.projects import service
from src.projects.schemas import (
    Project,
    ProjectCreate,
    ProjectPatch,
    ProjectUpdate,
)

router = APIRouter(prefix="/projects", tags=["Проекты"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Создать новый проект",
)
async def create_project(project: ProjectCreate):
    new_project = await service.create_project(project)

    headers = {"Location": f"{router.prefix}/{new_project['id']}"}
    return Response(status_code=status.HTTP_201_CREATED, headers=headers)


@router.get(
    "/",
    response_model=list[Project],
    status_code=status.HTTP_200_OK,
    summary="Получить список проектов",
)
async def get_projects(response: Response):
    db_projects = await service.get_projects()

    response.headers["Content-Location"] = router.prefix
    return db_projects


@router.get(
    "/{project_id}",
    response_model=Project,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": None},
    },
    summary="Получить проект по id",
)
async def get_project_by_id(project_id: PathParamId, response: Response):
    db_project = await service.get_project_by_id(project_id)

    if db_project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    response.headers["Content-Location"] = f"{router.prefix}/{project_id}"
    return db_project


@router.put(
    "/",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Заменить данные всех проектов",
)
async def update_all_projects(project: ProjectUpdate):
    db_projects = await service.get_projects()

    if db_projects:
        await service.update_all_projects(project)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# SELECT setval('project_id_seq', (SELECT COALESCE(MAX(id), 0) FROM "project"));
@router.put(
    "/{project_id}",
    response_model=Project,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_201_CREATED: {"model": None},
        status.HTTP_204_NO_CONTENT: {"model": None},
    },
    summary="Заменить данные проекта или создать новый",
)
async def update_project(
    project_id: PathParamId, project: ProjectUpdate, response: Response
):
    db_project = await service.get_project_by_id(project_id)

    # Если нет, создаем нового с таким id
    if db_project is None:
        await service.create_project(project, project_id)

        headers = {"Location": f"{router.prefix}/{project_id}"}
        return Response(status_code=status.HTTP_201_CREATED, headers=headers)
    else:
        response.headers["Content-Location"] = f"{router.prefix}/{project_id}"

    # Если нет изменений, возвращем 204
    put_fields = project.model_dump()
    if all(put_fields[key] == db_project[key] for key in put_fields):
        return Response(
            status_code=status.HTTP_204_NO_CONTENT, headers=response.headers
        )

    # Если есть, обновляем
    updated_project = await service.update_project(project, project_id)
    return updated_project


@router.delete(
    "/",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить все проекты",
)
async def delete_all_projects():
    await service.delete_all_projects()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
    "/{project_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": None},
    },
    summary="Удалить проект",
)
async def delete_project(project_id: PathParamId):
    db_project = await service.get_project_by_id(project_id)

    if db_project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    await service.delete_project(project_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch(
    "/",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Изменить данные всех проектов",
)
async def patch_all_projects(project: ProjectPatch):
    db_projects = await service.get_projects()

    if db_projects:
        await service.update_all_projects(project)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch(
    "/{project_id}",
    response_model=Project,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_204_NO_CONTENT: {"model": None},
        status.HTTP_404_NOT_FOUND: {"model": None},
    },
    summary="Изменить данные проекта",
)
async def patch_project(
    project_id: PathParamId, project: ProjectPatch, response: Response
):
    db_project = await service.get_project_by_id(project_id)

    # Если нет, 404
    if db_project is None:
        raise HTTPException(status_code=404)
    else:
        response.headers["Content-Location"] = f"{router.prefix}/{project_id}"

    # Если нет изменений, возвращем 204
    patch_fields = project.model_dump(exclude_unset=True)
    if all(patch_fields[key] == db_project[key] for key in patch_fields):
        return Response(
            status_code=status.HTTP_204_NO_CONTENT, headers=response.headers
        )

    # Если есть, обновляем
    db_project = await service.update_project(project, project_id)

    return db_project
