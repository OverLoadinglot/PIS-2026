from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from .value_objects import Money

@dataclass(frozen=True)
class DomainEvent:
    occurred_at: datetime = datetime.now()

@dataclass(frozen=True)
class TransactionAddedEvent(DomainEvent):
    budget_id: str
    transaction_id: str
    amount: Money
    category_name: str
    member_name: str
    is_expense: bool

@dataclass(frozen=True)
class LimitExceededEvent(DomainEvent):
    budget_id: str
    category_name: str
    limit_amount: Money
    actual_amount: Money
    exceeded_by: Money

@dataclass(frozen=True)
class BudgetArchivedEvent(DomainEvent):
    budget_id: str