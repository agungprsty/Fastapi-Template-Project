from fastapi import FastAPI
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager

from core.di import CoreContainer
from config.config import Settings
from src.utils.documents_loader import collect_documents


class BeanieLifespanFactory:
    def __init__(self, document_package: str):
        self.document_package = document_package

    @asynccontextmanager
    async def __call__(self, app: FastAPI):
        # Init DI Container
        container: CoreContainer = CoreContainer()
        container.wire(packages=["src"])
        app.container = container

        # Load settings
        settings: Settings = container.config()

        # Init MongoDB client
        client = AsyncIOMotorClient(
            host=settings.mongo.host,
            port=settings.mongo.port,
            username=settings.mongo.username,
            password=settings.mongo.password,
            authSource=settings.mongo.authSource
        )

        # Load all Beanie documents
        document_models = collect_documents(self.document_package)

        # Init Beanie
        await init_beanie(
            database=client[settings.mongo.db],
            document_models=document_models
        )

        app.state.mongo_client = client
        print("[MongoDB] Beanie Connected and initialized")

        yield  # 🔄 Allow app to start & serve

        # Shutdown: close connection
        client.close()
        print("[MongoDB] Beanie connection closed")
