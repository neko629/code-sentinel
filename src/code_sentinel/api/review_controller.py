import logging

from fastapi import APIRouter, HTTPException

from code_sentinel.core.review_service import review_service
from code_sentinel.schemas.review_dto import ReviewRequest, ReviewResponse

# create a router
router = APIRouter()

logger = logging.getLogger(__name__)

@router.post("/review", response_model=ReviewResponse)
def create_review(request: ReviewRequest):
    """
    post task of review

    receive code, language in request body, return review comments
    """
    logger.info(f"receive review request for file: {request.file_path}"
                f", language: {request.language}")

    try:
        ai_comments = review_service.review_code(
            code_diff=request.diff_content,
            language=request.language
        )
        return ReviewResponse(comments=ai_comments)
    except Exception as e:
        logger.error(f"error during code review: {e}")
        raise HTTPException(status_code=500, detail="Code review failed") from e
