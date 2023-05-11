import logging
from datetime import datetime
from http import HTTPStatus
from typing import NoReturn

import orjson
from fastapi import HTTPException
from starlette.responses import JSONResponse

from src.brokers.base import BaseProducer
from src.brokers.exceptions import ProducerError
from src.brokers.models import UserViewProgressEventModel
from src.services.base import BaseService


logger = logging.getLogger(__name__)


class UserActivityService(BaseService):
    def __init__(self, producer: BaseProducer):
        self._producer = producer

    async def send(self, key: bytes, value: bytes) -> NoReturn:
        await self._producer.send(key=key, value=value)

    async def save_view_progress(
        self, film_id: str, viewed_frame: int, user_id: str
    ) -> NoReturn:
        view_progress = UserViewProgressEventModel(
            user_id=user_id,
            film_id=film_id,
            viewed_frame=viewed_frame,
            event_time=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )

        try:
            key = f"{film_id}:{user_id}".encode("utf-8")
            await self.send(
                value=orjson.dumps(view_progress.dict()),
                key=key,
            )
        except ProducerError:
            logger.warning(
                "Error sending the event: film_id %s user_id %s",
                film_id,
                user_id,
                exc_info=True,
            )
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Error sending the event",
            )

        return JSONResponse(content={"result": "Ok."})
