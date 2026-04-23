from src.application.command.commands import CreateBudgetCommand
from src.application.ports.repository import BudgetRepository
from src.domain import FamilyBudget


class CreateBudgetHandler:
    def __init__(self, repository: BudgetRepository):
        self.repository = repository

    def handle(self, command: CreateBudgetCommand) -> str:
        budget = FamilyBudget(command.budget_id, command.name)
        self.repository.save(budget)
        return budget.id
