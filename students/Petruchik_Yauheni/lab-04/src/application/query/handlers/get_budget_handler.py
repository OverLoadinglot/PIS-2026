from src.application.query.queries import GetBudgetByIdQuery, BudgetReadDto
from src.application.ports.repository import BudgetRepository


class GetBudgetByIdHandler:
    def __init__(self, repository: BudgetRepository):
        self.repository = repository

    def handle(self, query: GetBudgetByIdQuery) -> BudgetReadDto:
        budget = self.repository.get_by_id(query.budget_id)
        if budget is None:
            raise ValueError(f"Бюджет с ID {query.budget_id} не найден")

        return BudgetReadDto(
            id=budget.id,
            name=budget.name,
            members_count=len(budget.get_members()),
            categories_count=len(budget.get_categories()),
            transactions_count=len(budget.get_transactions()),
            is_archived=getattr(budget, '_is_archived', False),
        )
