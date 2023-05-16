import random
from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_kafka_request(aiohttp_session, event_consumer):
    # Отправляем черех API просмотренный фрейм
    film_id = "dc3825a9-8668-400e-b083-97aa24081352"
    host = "http://localhost:8000/api/v1/view_progress/" + film_id
    user_id = "1ff75749-a557-44e4-a99e-4cbe2ca77534"
    body = {"user_id": user_id, "viewed_frame": random.randint(1, 1000)}
    async with aiohttp_session.post(host, json=body) as resp:
        assert resp.status == HTTPStatus.OK

    # Подключаемся к кафке и смотрим, что там появилось событие
    events = dict()
    for event in event_consumer:
        events[event.key] = event.value

    assert events[f"{film_id}:{user_id}"] == body["viewed_frame"]