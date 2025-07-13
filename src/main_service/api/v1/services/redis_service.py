import redis.asyncio as redis


class RedisService:
    def __init__(self, host="localhost", port=6379):
        self.client = redis.Redis(host=host,
                                  port=port,
                                  db=0,
                                  decode_responses=True)

    async def save_auth_token(self, chat_id: int, token: str, ttl: int = 3600):
        await self.client.hset(f"auth:{chat_id}",
                               mapping={"access_token": token})
        await self.client.expire(f"auth:{chat_id}", ttl)

    async def get_auth_token(self, chat_id: int) -> str | None:
        return await self.client.hget(f"auth:{chat_id}", "access_token")

    async def delete_auth_token(self, chat_id: int):
        await self.client.delete(f"auth:{chat_id}")
