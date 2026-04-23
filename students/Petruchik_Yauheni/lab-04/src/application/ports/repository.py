from abc import ABC, abstractmethod


class BudgetRepository(ABC):
    @abstractmethod
    def get_by_id(self, budget_id: str):
        raise NotImplementedError

    @abstractmethod
    def save(self, budget):
        raise NotImplementedError
