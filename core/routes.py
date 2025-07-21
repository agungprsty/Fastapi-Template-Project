from typing import Union
from fastapi import APIRouter
from src.routes.user import user_routes

root_router = APIRouter(
    prefix="/api/v2"
)

@root_router.get("/")
async def read_root():
    return {"Hello": "World"}

@root_router.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


routers: tuple[APIRouter, ...] = (
    user_routes,
    )

for router in routers:
    root_router.include_router(router)