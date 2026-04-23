from dataclasses import dataclass


@dataclass
class BudgetSummaryView:
    budget_id: str
    name: str
    members_count: int
    categories_count: int
    transactions_count: int
