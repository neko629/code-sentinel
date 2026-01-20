import logging

from fastapi import FastAPI

from code_sentinel.api.review_controller import router as review_router
from code_sentinel.api.webhook_controller import router as webhook_router

logging.basicConfig(level=logging.INFO)

def create_app() -> FastAPI:
    app = FastAPI(
        title="CodeSentinel API",
        description="Code Sentinel API",
        version="0.1.0"
    )

    app.include_router(review_router, prefix="/api/v1", tags=["review"])
    app.include_router(webhook_router, prefix="/api/v1", tags=["webhook"])
    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
    #poetry run uvicorn code_sentinel.main:app --reload
