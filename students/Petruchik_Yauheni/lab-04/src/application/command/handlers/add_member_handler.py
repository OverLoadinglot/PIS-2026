from src.application.command.commands import AddMemberCommand
from src.application.ports.repository import BudgetRepository
from src.domain import FamilyMember


class AddMemberHandler:
    def __init__(self, repository: BudgetRepository):
        self.repository = repository

    def handle(self, command: AddMemberCommand) -> None:
        budget = self.repository.get_by_id(command.budget_id)
        if budget is None:
            raise ValueError(f"Бюджет с ID {command.budget_id} не найден")
        budget.add_member(FamilyMember(command.member_id, command.member_name))
        self.repository.save(budget)
