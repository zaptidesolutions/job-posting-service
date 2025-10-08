from abc import ABC, abstractmethod

class JobFilterStrategy(ABC):
    @abstractmethod
    def build_query(self) -> dict:
        pass

    @abstractmethod
    def build_sort(self) -> list:
        pass
