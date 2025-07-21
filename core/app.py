from fastapi import FastAPI
from config.config import Settings
from core.routes import root_router
from core.lifespan import BeanieLifespanFactory
from core.di import CoreContainer
from core.error import register_exception_handlers


def make_app() -> FastAPI:
    container = CoreContainer()
    settings: Settings = container.config()

    lifespan = BeanieLifespanFactory("src.infrastructure.document")

    app = FastAPI(
        title=settings.app_name,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan
    )

    register_exception_handlers(app)
    
    app.include_router(root_router)

    return app

app = make_app()
