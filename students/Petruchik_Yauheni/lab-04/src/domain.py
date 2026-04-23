from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Dict, List, Optional


class BudgetException(Exception):
    pass


class MemberNotFoundException(BudgetException):
    pass


class CategoryNotFoundException(BudgetException):
    pass


class BudgetAlreadyArchivedException(BudgetException):
    pass


class LimitExceededException(BudgetException):
    pass


class TransactionType:
    INCOME = "income"
    EXPENSE = "expense"


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

    def __sub__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Нельзя вычитать деньги в разных валютах")
        return Money(self.amount - other.amount, self.currency)


@dataclass(frozen=True)
class DateRange:
    start: date
    end: date

    def __post_init__(self):
        if self.start > self.end:
            raise ValueError("Дата начала не может быть позже даты окончания")

    def contains(self, value: date) -> bool:
        return self.start <= value <= self.end


@dataclass(frozen=True)
class FamilyMember:
    id: str
    name: str


@dataclass(frozen=True)
class Category:
    id: str
    name: str


@dataclass(frozen=True)
class Transaction:
    id: str
    amount: Money
    type: str
    category_id: str
    member_id: str
    date: date
    description: str = ""


@dataclass(frozen=True)
class DomainEvent:
    pass


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
    limit: Money
    spent: Money
    exceeded: Money


@dataclass(frozen=True)
class BudgetArchivedEvent(DomainEvent):
    budget_id: str


@dataclass
class BudgetLimit:
    category_id: str
    limit_amount: Money
    period: DateRange


class FamilyBudget:
    def __init__(self, budget_id: str, name: str):
        self.id = budget_id
        self.name = name
        self._members: Dict[str, FamilyMember] = {}
        self._categories: Dict[str, Category] = {}
        self._limits: List[BudgetLimit] = []
        self._transactions: Dict[str, Transaction] = {}
        self._is_archived = False
        self._events: List[DomainEvent] = []

    def add_member(self, member: FamilyMember):
        if self._is_archived:
            raise BudgetAlreadyArchivedException("Нельзя изменять архивный бюджет")
        self._members[member.id] = member

    def add_category(self, category: Category):
        if self._is_archived:
            raise BudgetAlreadyArchivedException("Нельзя изменять архивный бюджет")
        self._categories[category.id] = category

    def set_limit(self, category_id: str, limit_amount: Money, period: DateRange):
        if self._is_archived:
            raise BudgetAlreadyArchivedException("Нельзя изменять архивный бюджет")
        if category_id not in self._categories:
            raise CategoryNotFoundException(f"Категория {category_id} не найдена")
        self._limits = [limit for limit in self._limits if not (limit.category_id == category_id and self._periods_overlap(limit.period, period))]
        self._limits.append(BudgetLimit(category_id, limit_amount, period))

    def add_transaction(self, transaction: Transaction):
        if self._is_archived:
            raise BudgetAlreadyArchivedException("Нельзя изменять архивный бюджет")
        if transaction.member_id not in self._members:
            raise MemberNotFoundException(f"Член семьи {transaction.member_id} не найден")
        if transaction.category_id not in self._categories:
            raise CategoryNotFoundException(f"Категория {transaction.category_id} не найдена")
        if transaction.type == TransactionType.EXPENSE:
            limit = self._get_limit_for_category_at_date(transaction.category_id, transaction.date)
            if limit is not None:
                spent_before = self._calculate_spent_for_category_in_period(transaction.category_id, limit.period)
                if (spent_before + transaction.amount).amount > limit.limit_amount.amount:
                    exceeded = (spent_before + transaction.amount) - limit.limit_amount
                    self._events.append(LimitExceededEvent(
                        self.id,
                        self._categories[transaction.category_id].name,
                        limit.limit_amount,
                        spent_before + transaction.amount,
                        exceeded
                    ))
                    raise LimitExceededException("Превышен лимит по категории")
        self._transactions[transaction.id] = transaction
        self._events.append(TransactionAddedEvent(
            self.id,
            transaction.id,
            transaction.amount,
            self._categories[transaction.category_id].name,
            self._members[transaction.member_id].name,
            transaction.type == TransactionType.EXPENSE
        ))

    def archive(self):
        if not self._is_archived:
            self._is_archived = True
            self._events.append(BudgetArchivedEvent(self.id))

    def pull_events(self) -> List[DomainEvent]:
        events = self._events.copy()
        self._events.clear()
        return events

    def get_transactions(self) -> List[Transaction]:
        return list(self._transactions.values())

    def get_members(self) -> List[FamilyMember]:
        return list(self._members.values())

    def get_categories(self) -> List[Category]:
        return list(self._categories.values())

    @staticmethod
    def _periods_overlap(first: DateRange, second: DateRange) -> bool:
        return not (first.end < second.start or second.end < first.start)

    def _get_limit_for_category_at_date(self, category_id: str, target_date: date) -> Optional[BudgetLimit]:
        for limit in self._limits:
            if limit.category_id == category_id and limit.period.contains(target_date):
                return limit
        return None

    def _calculate_spent_for_category_in_period(self, category_id: str, period: DateRange) -> Money:
        total = Money(0, "RUB")
        for transaction in self._transactions.values():
            if transaction.category_id == category_id and transaction.type == TransactionType.EXPENSE and period.contains(transaction.date):
                total = total + transaction.amount
        return total
