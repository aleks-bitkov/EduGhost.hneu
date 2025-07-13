from abc import ABC, abstractmethod


class IService(ABC):

    def __init__(self):
        self.data = {}

    @abstractmethod
    def save(self, e) -> None: ...

    @abstractmethod
    def get(self, *args): ...