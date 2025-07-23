from abc import ABC, abstractmethod


class TriggerBaseClass(ABC):
    @abstractmethod
    def __call__(self, payload: dict, params: dict) -> bool: ...

    @classmethod
    def describe(cls) -> dict: ...
