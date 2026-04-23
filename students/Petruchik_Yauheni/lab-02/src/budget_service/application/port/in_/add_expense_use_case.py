from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class AddExpenseCommand:
    """Входящий DTO (Data Transfer Object) с данными для создания расхода"""
    amount: float
    category_id: str
    user_id: str
    description: str

class AddExpenseUseCase(ABC):
    """Входящий порт: добавление нового расхода"""
    
    @abstractmethod
    def execute(self, command: AddExpenseCommand) -> str:
        """Создает расход и возвращает его ID"""
        pass