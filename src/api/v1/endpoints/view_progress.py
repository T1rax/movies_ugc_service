from http import HTTPStatus
from typing import Optional

import dpath
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi_pagination import Page

from src.api.v1.models.responses import InternalServerError, NotFound
from src.api.v1.models.view_progress import (
    FilmView,
    SaveViewProgressInput,
    ViewProgress,
)
from src.common.decode_auth_token import get_decoded_data
from src.containers import Container
from src.services.user_view_history import UserViewHistoryService


router = APIRouter()


@router.post(
    "/view_progress",
    responses={404: {"model": NotFound}, 500: {"model": InternalServerError}},
    summary="Сохранение временной метки о просмотре фильма.",
    description="Отправить сообщение с временной меткой о просмотре фильма в топик брокера сообщений.",
)
@inject
async def saving_view_progress(
    body: SaveViewProgressInput = Body(...),
    user_view_service: UserViewHistoryService = Depends(
        Provide[Container.user_view_history_service]
    ),
    user_data=Depends(get_decoded_data),
) -> JSONResponse:
    user_id = dpath.get(user_data, "user_id", default=None)
    if not user_id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Undefined user.",
        )
    user_view_progress_data = ViewProgress(
        film_id=body.film_id,
        viewed_frame=body.viewed_frame,
        user_id=user_id,  # type: ignore[arg-type]
    )

    await user_view_service.insert_or_update_view_progress(
        user_view_progress_data
    )

    return await user_view_service.send_view_progress(user_view_progress_data)


@router.get(
    "/view_progress",
    response_model=ViewProgress,
    responses={404: {"model": NotFound}},
    summary="Получение временной метки о просмотре фильма.",
    description="Получить временную метку о просмотре фильма, на которой остановился пользователь.",
)
@inject
async def get_view_progress(
    film_id: str,
    user_view_service: UserViewHistoryService = Depends(
        Provide[Container.user_view_history_service]
    ),
    user_data=Depends(get_decoded_data),
) -> Optional[ViewProgress]:
    user_id = dpath.get(user_data, "user_id", default=None)
    if not user_id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Undefined user.",
        )

    return await user_view_service.get_last_view_progress(
        dict(user_id=user_id, film_id=film_id)
    )


@router.get(
    "/watching_now",
    summary="Список фильмов которые сейчас смотрят.",
    description="Список film_id которые пользователи сейчас смотрят, отсортированный по количеству пользователей.",
)
@inject
async def watching_now(
    user_view_service: UserViewHistoryService = Depends(
        Provide[Container.user_view_history_service]
    ),
) -> Page[FilmView]:
    res = await user_view_service.get_films_ids_watching_now()
    return res
