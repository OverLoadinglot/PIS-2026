from dataclasses import dataclass
from datetime import date
from typing import Dict, List

from src.domain.models.exceptions import (
    BudgetAlreadyArchivedException,
    CategoryNotFoundException,
    MemberNotFoundException,
    LimitExceededException,
)


@dataclass(frozen=True)
class Money:
    amount: float
    currency: str = "RUB"

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Сумма не может быть отрицательной")
        if not self.currency or not self.currency.strip():
            raise ValueError("Валюта не может быть пустой")

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Нельзя складывать деньги в разных валютах")
        return Money(self.amount + other.amount, self.currency)


@dataclass(frozen=True)
class Transaction:
    id: str
    amount: Money
    type: str
    category_id: str
    member_id: str
    date: date
    description: str = ""


@dataclass
class FamilyBudget:
    id: str
    name: str
    members: Dict[str, str]
    categories: Dict[str, str]
    transactions: Dict[str, Transaction]
    is_archived: bool = False
    _events: List = None

    def __post_init__(self):
        self.members = self.members or {}
        self.categories = self.categories or {}
        self.transactions = self.transactions or {}
        self._events = []

    def add_member(self, member_id: str, name: str):
        if self.is_archived:
            raise BudgetAlreadyArchivedException("Нельзя изменять архивный бюджет")
        self.members[member_id] = name

    def add_category(self, category_id: str, name: str):
        if self.is_archived:
            raise BudgetAlreadyArchivedException("Нельзя изменять архивный бюджет")
        self.categories[category_id] = name

    def add_transaction(self, transaction: Transaction):
        if self.is_archived:
            raise BudgetAlreadyArchivedException("Нельзя изменять архивный бюджет")
        if transaction.member_id not in self.members:
            raise MemberNotFoundException(f"Член семьи {transaction.member_id} не найден")
        if transaction.category_id not in self.categories:
            raise CategoryNotFoundException(f"Категория {transaction.category_id} не найдена")
        if transaction.type == "expense":
            self.transactions[transaction.id] = transaction
            self._events.append({"type": "TransactionAdded", "id": transaction.id})
        else:
            self.transactions[transaction.id] = transaction
            self._events.append({"type": "TransactionAdded", "id": transaction.id})

    def pull_events(self):
        events = list(self._events)
        self._events.clear()
        return events

    def get_members(self):
        return list(self.members.items())

    def get_categories(self):
        return list(self.categories.items())

    def get_transactions(self):
        return list(self.transactions.values())
