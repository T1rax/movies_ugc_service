from http import HTTPStatus

import pytest
from fastapi import HTTPException

from src.services.user_view_history import UserViewHistoryService
from tests.fake.services import FakeProducer, FakeUARepository


async def test_last_view_progress(frame_data):
    producer = FakeProducer()
    repository = FakeUARepository()

    # Добавляем фейковые данные
    viewed_frame = frame_data.viewed_frame
    document_data = dict()
    document_data[f"{frame_data.film_id}:{frame_data.user_id}"] = frame_data
    repository.storage["view_progress"] = document_data

    service = UserViewHistoryService(producer, repository)

    filter_ = dict(film_id=frame_data.film_id, user_id=frame_data.user_id)

    result = await service.get_last_view_progress(filter_)

    assert result.viewed_frame == viewed_frame


async def test_last_view_progress_no_data(frame_data):
    producer = FakeProducer()
    repository = FakeUARepository()
    service = UserViewHistoryService(producer, repository)

    filter_ = dict(film_id=frame_data.film_id, user_id=frame_data.user_id)

    with pytest.raises(HTTPException) as e_info:
        await service.get_last_view_progress(filter_)

    assert e_info.value.status_code == HTTPStatus.NOT_FOUND
