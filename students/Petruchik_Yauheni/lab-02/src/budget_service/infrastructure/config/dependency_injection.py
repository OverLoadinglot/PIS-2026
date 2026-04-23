from budget_service.infrastructure.adapter.out.in_memory_expense_repository import InMemoryExpenseRepository
from budget_service.infrastructure.adapter.out.console_notification_adapter import ConsoleNotificationAdapter
from budget_service.application.service.expense_service import ExpenseService

class DependencyContainer:
    """Скелет DI-контейнера: связывание портов и адаптеров"""
    
    def __init__(self):
        # 1. Создаем экземпляры адаптеров (Infrastructure)
        self.expense_repository = InMemoryExpenseRepository()
        self.notification_service = ConsoleNotificationAdapter()
        
        # 2. Создаем Application сервис с инъекцией зависимостей
        self.expense_service = ExpenseService(
            repository=self.expense_repository,
            notification_service=self.notification_service
        )
        
    def get_expense_service(self) -> ExpenseService:
        """Возвращает готовый к работе сервис"""
        return self.expense_service