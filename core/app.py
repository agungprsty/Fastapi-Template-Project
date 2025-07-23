from fastapi import FastAPI
from config.config import Settings
from core.routes import root_router, api_router
from core.lifespan import LifespanFactory
from core.di import CoreContainer
from core.error import register_exception_handlers
from core.logger import configure_logging


def make_app() -> FastAPI:
    container = CoreContainer()
    settings: Settings = container.config()

    lifespan = LifespanFactory()

    # FastAPI app setup
    app = FastAPI(
        title=settings.app_name,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan
    )

    # Logging setup
    configure_logging(app)

    # Exception handlers
    register_exception_handlers(app)
    
    # Router
    app.include_router(root_router)
    app.include_router(api_router)

    return app

app = make_app()
