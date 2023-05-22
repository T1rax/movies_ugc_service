import logging
from datetime import datetime
from http import HTTPStatus
from typing import NoReturn

import dpath
import orjson
from fastapi import HTTPException
from pymongo.errors import ServerSelectionTimeoutError
from starlette.responses import JSONResponse

from src.api.v1.models.bookmarks import UserBookmark
from src.brokers.base import BaseProducer
from src.brokers.exceptions import ProducerError
from src.repositories.base import BaseRepository
from src.services.base import BaseService


logger = logging.getLogger(__name__)


class UserBookmarksService(BaseService):
    def __init__(self, producer: BaseProducer, repository: BaseRepository):
        self._producer = producer
        self._repository = repository

    async def send(self, key: bytes, value: bytes) -> NoReturn:
        await self._producer.send(key=key, value=value)

    async def send_event_bookmark(self, data: dict) -> NoReturn:
        user_id = dpath.get(data, "user_id", default=None)
        film_id = dpath.get(data, "film_id", default=None)
        event_type = dpath.get(data, "event_type", default=None)
        if not user_id or not film_id:
            logger.warning(
                "Error send new_bookmark: user_id %s film_id %s event_type %s.",
                user_id,
                film_id,
                event_type,
            )
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Error sending the event",
            )

        view_progress = UserBookmark(
            user_id=user_id,
            film_id=film_id,
            event_type=event_type,
            ts=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )

        try:
            key = f"{film_id}:{user_id}".encode("utf-8")
            await self.send(
                value=orjson.dumps(view_progress.dict()),
                key=key,
            )
        except ProducerError:
            logger.warning(
                "Error sending the event: film_id %s user_id %s event_type %s",
                film_id,
                user_id,
                event_type,
                exc_info=True,
            )
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Error sending the event",
            )

        return JSONResponse(content={"result": "Ok."})

    async def insert_or_update_bookmark(
        self, data: dict, is_deleted: bool = False
    ) -> NoReturn:
        table_name = "user_bookmarks"
        user_id = dpath.get(data, "user_id", default=None)
        film_id = dpath.get(data, "film_id", default=None)
        if not user_id or not film_id:
            logger.warning(
                "Error insert or update user bookmark: table_name %s user_id %s film_id %s.",
                table_name,
                user_id,
                film_id,
            )
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Error save bookmark",
            )

        filter_query = dict(film_id=film_id, user_id=user_id)
        try:
            await self._repository.upsert(
                filter_=filter_query,
                key="is_deleted",
                value=is_deleted,
                table_name=table_name,
            )
        except ServerSelectionTimeoutError:
            logger.error(
                "MongoDb Error. Failed to create or update a user bookmark: filter_query %s, table_name %s",
                filter_query,
                table_name,
                exc_info=True,
            )