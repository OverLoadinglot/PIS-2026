from src.application.command.commands import AddCategoryCommand
from src.application.ports.repository import BudgetRepository
from src.domain import Category


class AddCategoryHandler:
    def __init__(self, repository: BudgetRepository):
        self.repository = repository

    def handle(self, command: AddCategoryCommand) -> None:
        budget = self.repository.get_by_id(command.budget_id)
        if budget is None:
            raise ValueError(f"Бюджет с ID {command.budget_id} не найден")
        budget.add_category(Category(command.category_id, command.category_name))
        self.repository.save(budget)
