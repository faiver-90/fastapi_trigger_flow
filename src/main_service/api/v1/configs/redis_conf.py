import redis.asyncio as redis
from typing import Optional


class RedisService:
    def __init__(self, url: str):
        self.client = redis.from_url(url, decode_responses=True)

    async def get(self, key: str) -> Optional[str]:
        return await self.client.get(key)

    async def set(self, key: str, value: str, ex: int = 3600):
        await self.client.set(key, value, ex=ex)

    async def delete(self, key: str):
        await self.client.delete(key)

    async def exists(self, key: str):
        return await self.client.exists(key) == 1


# redis_service = RedisService(url="redis://localhost:6379/0")
redis_service = RedisService(url="redis://reddis:6379/0")
