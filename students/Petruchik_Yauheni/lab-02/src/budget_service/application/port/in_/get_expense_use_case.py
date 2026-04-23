from abc import ABC, abstractmethod

class GetExpenseUseCase(ABC):
    """Входящий порт: получение расхода по ID"""
    
    @abstractmethod
    def get(self, expense_id: str):
        """Возвращает объект Expense или None"""
        pass