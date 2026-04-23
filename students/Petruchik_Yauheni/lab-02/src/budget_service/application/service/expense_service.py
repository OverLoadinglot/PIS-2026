from budget_service.application.port.in_.add_expense_use_case import AddExpenseUseCase, AddExpenseCommand
from budget_service.application.port.in_.get_expense_use_case import GetExpenseUseCase
from budget_service.application.port.out.expense_repository import ExpenseRepository
from budget_service.application.port.out.notification_service import NotificationService

class ExpenseService(AddExpenseUseCase, GetExpenseUseCase):
    """
    Реализация use-cases для управления расходами.
    Центральный элемент Application слоя.
    """
    
    # Внедрение зависимостей (Dependency Injection) через конструктор
    def __init__(self, repository: ExpenseRepository, notification_service: NotificationService):
        self.repository = repository
        self.notification_service = notification_service

    def execute(self, command: AddExpenseCommand) -> str:
        # TODO: Реализовать в Lab #4 (создание Expense, сохранение в repo, отправка уведомления)
        raise NotImplementedError("Бизнес-логика будет реализована в Lab #4")

    def get(self, expense_id: str):
        # TODO: Реализовать в Lab #4 (вызов self.repository.find_by_id)
        raise NotImplementedError("Бизнес-логика будет реализована в Lab #4")