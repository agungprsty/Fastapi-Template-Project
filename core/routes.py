from typing import Union
from fastapi import APIRouter
from datetime import datetime
from fastapi import APIRouter, Request
from src.routes.user import user_routes
from src.infrastructure.task.send_reminder import send_reminder

root_router = APIRouter()
api_router = APIRouter(
    prefix="/api/v1"
)

@root_router.get("/")
async def read_root():
    return {"Hello": "World"}

@api_router.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@api_router.post("/interval")
async def apscheduler_demo(request: Request, message: str):
    scheduler = request.app.state.scheduler
    scheduler.add_job(
        send_reminder,
        'interval',
        minutes=1,
        kwargs={"message": message},
        id=f"reminder-{int(datetime.now().timestamp())}",
        replace_existing=True
    )
    return {"status": "scheduled 1 minutes"}

@api_router.get("/cache")
async def cache_demo(request: Request, message: str):
    redis = request.app.state.redis
    await redis.set("example", message, ex=120)
    val = await redis.get("example")
    return {"value": val, "expire": 120}

api_routers: tuple[APIRouter, ...] = (
    user_routes,
)

for router in api_routers:
    api_router.include_router(router)