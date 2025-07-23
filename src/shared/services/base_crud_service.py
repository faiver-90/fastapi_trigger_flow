from typing import Generic, TypeVar

RepoType = TypeVar("RepoType")


class BaseCRUDService(Generic[RepoType]):
    def __init__(self, repo: RepoType):
        self.repo = repo

    async def create(self, data):
        return await self.repo.create(data)

    async def get(self, obj_id: int):
        return await self.repo.get(obj_id)

    async def list(self):
        return await self.repo.list()

    async def update(self, obj_id: int, data):
        return await self.repo.update(obj_id, data)

    async def delete(self, obj_id: int):
        return await self.repo.delete(obj_id)
