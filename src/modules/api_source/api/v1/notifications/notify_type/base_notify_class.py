from abc import abstractmethod, ABC


class NotificationBaseClass(ABC):
    @abstractmethod
    async def send(self, payload: dict, config: dict):  ...
