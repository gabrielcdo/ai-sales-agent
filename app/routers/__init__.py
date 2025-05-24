from fastapi import APIRouter
from starlette.responses import JSONResponse
from starlette.responses import RedirectResponse

from app.core.settings import Settings
from app.routers import ai_agent

settings = Settings()
router = APIRouter(prefix=settings.prefix)
router.include_router(ai_agent.router)


@router.get("/")
async def docs_redirect():
    return RedirectResponse(url=settings.prefix + "/docs")


@router.get("/healthcheck")
async def healthcheck():
    return JSONResponse({"message": "OK"})
