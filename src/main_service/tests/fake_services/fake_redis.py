class FakeRedis:
    def __init__(self):
        self.storage = {}

    async def get(self, key):
        return self.storage.get(key)

    async def set(self, key, value):
        self.storage[key] = value

    async def delete(self, key):
        self.storage.pop(key, None)

    async def exists(self, key):
        return key in self.storage
