from abc import ABC, abstractmethod

class JobQueryStrategy(ABC):
    @abstractmethod
    def apply(self, query: dict, sort: list) -> tuple[dict, list]:
        """
        Apply filtering to the query and optionally modify the sort order.
        Returns a tuple: (query_dict, sort_list)
        """
        pass
