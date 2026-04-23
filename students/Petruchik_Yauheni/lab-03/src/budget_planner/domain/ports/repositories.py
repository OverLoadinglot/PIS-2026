from abc import ABC, abstractmethod
from typing import Optional, List
from ..models.entities import FamilyBudget, Transaction

class FamilyBudgetRepository(ABC):
    @abstractmethod
    def save(self, budget: FamilyBudget) -> None:
        pass

    @abstractmethod
    def find_by_id(self, budget_id: str) -> Optional[FamilyBudget]:
        pass

    @abstractmethod
    def delete(self, budget_id: str) -> None:
        pass

class TransactionRepository(ABC):
    @abstractmethod
    def add(self, transaction: Transaction) -> None:
        pass

    @abstractmethod
    def find_by_budget(self, budget_id: str) -> List[Transaction]:
        pass