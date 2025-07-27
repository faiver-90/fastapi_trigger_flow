from abc import ABC, abstractmethod


class BaseTypeTriggerClass(ABC):
    @abstractmethod
    def __call__(self, payload: dict, params: dict) -> bool: ...

    @classmethod
    def describe(cls) -> dict: ...

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.describe()}"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.describe()}>"