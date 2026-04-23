from src.application.command.commands import SetLimitCommand
from src.application.ports.repository import BudgetRepository
from src.domain import DateRange, Money


class SetLimitHandler:
    def __init__(self, repository: BudgetRepository):
        self.repository = repository

    def handle(self, command: SetLimitCommand) -> None:
        budget = self.repository.get_by_id(command.budget_id)
        if budget is None:
            raise ValueError(f"Бюджет с ID {command.budget_id} не найден")

        budget.set_limit(
            command.category_id,
            Money(command.amount, command.currency),
            DateRange(command.start_date, command.end_date)
        )
        self.repository.save(budget)
