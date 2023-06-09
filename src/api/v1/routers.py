from fastapi import APIRouter

from src.api.v1.endpoints import (
    bookmarks,
    film_reviews,
    film_scores,
    review_likes,
    view_progress,
)


router = APIRouter(prefix="/api/v1", tags=["v1"])

router.include_router(bookmarks.router)
router.include_router(view_progress.router)
router.include_router(film_scores.router)
router.include_router(film_reviews.router)
router.include_router(review_likes.router)
