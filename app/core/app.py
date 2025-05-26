import logging
import time
import sentry_sdk

from fastapi import FastAPI
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.responses import Response

from app.core.resources import Resources
from app.core.settings import Settings
from app.routers import router

logger = logging.getLogger("uvicorn")

settings = Settings()


if settings.environment in ["prod", "dev"]:
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        environment=settings.environment.lower(),
        traces_sample_rate=1.0,
    )


def init_app(settings: Settings) -> FastAPI:
    exception_handlers = {
        RequestValidationError: invalid_data,
        Exception: internal_error,
    }

    app = FastAPI(
        title=settings.api_name,
        version=settings.api_version,
        docs_url=settings.prefix + "/docs",
        on_startup=[startup],
        exception_handlers=exception_handlers,
    )

    app.include_router(router)
    return app


async def invalid_data(_: Request, exc: Exception) -> Response:
    return JSONResponse(status_code=422, content={"error": str(exc)})


async def internal_error(_: Request, exc: Exception) -> Response:
    return JSONResponse(status_code=500, content={"error": str(exc)})


async def startup():
    logger.info("Initializing resources...")
    begin = time.time()
    Resources()
    end = time.time()
    timer = float(end - begin)
    logger.info(f"Resources initialization took {timer:.3f} seconds")
