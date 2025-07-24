from redis.asyncio import Redis
from config.config import Settings

class RedisConnection(object):
    def __init__(self, settings: Settings):
        self.__settings = settings

    def connect(self) -> Redis:
        return Redis(
            host=self.__settings.host,
            port=self.__settings.port,
            password=self.__settings.password,
            db=self.__settings.db,
        )
