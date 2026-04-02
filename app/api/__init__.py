from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core import AppConfig
from app.core.logger import logger
from app.core.response import JsonResponse


def create_app(config: AppConfig) -> FastAPI:
    logger.info_with("app start", "address", config.service.port)
    app = FastAPI(
        root_path="/api/v1",
        openapi_url="/api/v1/openapi.json",
        default_response_class=JsonResponse
    )

    def init_router():
        from app.api.v1.login import views as login_views
        app.include_router(login_views.router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    init_router()
    return app
