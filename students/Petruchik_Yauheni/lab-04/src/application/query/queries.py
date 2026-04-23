from dataclasses import dataclass


@dataclass(frozen=True)
class GetBudgetByIdQuery:
    budget_id: str


@dataclass(frozen=True)
class BudgetReadDto:
    id: str
    name: str
    members_count: int
    categories_count: int
    transactions_count: int
    is_archived: bool
