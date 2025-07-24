from abc import abstractmethod, ABC


class BaseTypeNotificationClass(ABC):
    @abstractmethod
    async def send(self, payload: dict, config: dict):  ...

    @classmethod
    def describe(cls) -> dict: ...
