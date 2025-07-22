from fastapi import FastAPI
from beanie import init_beanie
from pymongo import MongoClient
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.jobstores.mongodb import MongoDBJobStore

from core.di import CoreContainer
from config.config import Settings
from src.utils.documents_loader import collect_documents


class LifespanFactory:
    def __init__(self):
        self.document_package = "src.infrastructure.document"

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

        # Init APScheduler with MongoDBJobStore
        sync_client = MongoClient(
            host=settings.mongo.host,
            port=settings.mongo.port,
            username=settings.mongo.username,
            password=settings.mongo.password,
            authSource=settings.mongo.authSource
        )

        jobstores = {
            'default': MongoDBJobStore(
                database=settings.mongo.db,
                collection='apscheduler_jobs',
                client=sync_client  # pymongo client (sync)
            )
        }
        executors = {
            'default': AsyncIOExecutor()
        }

        scheduler = AsyncIOScheduler(
            jobstores=jobstores,
            executors=executors,
            job_defaults={'coalesce': False, 'max_instances': 3},
            timezone="Asia/Jakarta"
        )
        scheduler.start()
        app.state.scheduler = scheduler
        print("[Scheduler] APScheduler started")

        yield  # Run FastAPI app

        # Shutdown scheduler & mongo
        scheduler.shutdown()
        client.close()
        sync_client.close()
        print("[Scheduler] Stopped")
        print("[MongoDB] Closed")
