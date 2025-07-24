from redis.asyncio import Redis
from typing import Optional

class RedisClient:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get(self, key: str) -> Optional[str]:
        return await self.redis.get(key)

    async def set(self, key: str, value: str, expire: int = 3600) -> bool:
        return await self.redis.set(key, value, ex=expire)

    async def delete(self, key: str) -> int:
        return await self.redis.delete(key)
