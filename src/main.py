import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.api.files import file_router
from src.api.services import service_router
from src.api.users import user_router
from src.core import app_settings
from src.core.logging_config import logger

app = FastAPI(
    title=app_settings.title,
    default_response_class=ORJSONResponse,
    docs_url="/api",
    redoc_url=None,
)

app.include_router(user_router)
app.include_router(file_router)
app.include_router(service_router)

if __name__ == "__main__":
    logger.info(
        "Server is starting at %s:%s", app_settings.host, app_settings.port
    )
    uvicorn.run(
        "main:app",
        host=app_settings.host,
        port=app_settings.port,
        loop="asyncio",
        reload=True,
    )
