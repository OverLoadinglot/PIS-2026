from typing import List, Dict, Optional
from datetime import date
from .value_objects import Money, CategoryName, MemberName, DateRange, Percentage, TransactionType
from .events import DomainEvent, TransactionAddedEvent, LimitExceededEvent, BudgetArchivedEvent
from .exceptions import (
    LimitExceededException, InvalidTransactionException,
    MemberNotFoundException, CategoryNotFoundException, BudgetAlreadyArchivedException
)

# ----- Сущности -----
class FamilyMember:
    def __init__(self, member_id: str, name: MemberName, role: str = "member"):
        self.id = member_id
        self.name = name
        self.role = role  # e.g., "admin", "member"
        self.is_active = True

    def __eq__(self, other):
        if not isinstance(other, FamilyMember):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

class Category:
    def __init__(self, category_id: str, name: CategoryName, color: str = "#000000"):
        self.id = category_id
        self.name = name
        self.color = color

    def __eq__(self, other):
        if not isinstance(other, Category):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

class Transaction:
    def __init__(self, transaction_id: str, amount: Money, type: TransactionType,
                 category_id: str, member_id: str, date: date, description: str = ""):
        self.id = transaction_id
        self.amount = amount
        self.type = type
        self.category_id = category_id
        self.member_id = member_id
        self.date = date
        self.description = description

    def __eq__(self, other):
        if not isinstance(other, Transaction):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

# ----- Value Object для лимита (хранится внутри агрегата) -----
class BudgetLimit:
    def __init__(self, category_id: str, limit_amount: Money, period: DateRange):
        self.category_id = category_id
        self.limit_amount = limit_amount
        self.period = period

# ----- Aggregate Root: FamilyBudget -----
class FamilyBudget:
    def __init__(self, budget_id: str, name: str):
        self.id = budget_id
        self.name = name
        self._members: Dict[str, FamilyMember] = {}
        self._categories: Dict[str, Category] = {}
        self._transactions: Dict[str, Transaction] = {}
        self._limits: List[BudgetLimit] = []
        self._is_archived = False
        self._events: List[DomainEvent] = []

    # --- Управление членами семьи ---
    def add_member(self, member: FamilyMember):
        if self._is_archived:
            raise BudgetAlreadyArchivedException("Нельзя изменять архивный бюджет")
        if member.id in self._members:
            raise InvalidTransactionException(f"Член семьи {member.id} уже существует")
        self._members[member.id] = member

    def get_member(self, member_id: str) -> FamilyMember:
        if member_id not in self._members:
            raise MemberNotFoundException(f"Член семьи {member_id} не найден")
        return self._members[member_id]

    # --- Управление категориями ---
    def add_category(self, category: Category):
        if self._is_archived:
            raise BudgetAlreadyArchivedException("Нельзя изменять архивный бюджет")
        if category.id in self._categories:
            raise InvalidTransactionException(f"Категория {category.id} уже существует")
        # Уникальность имени (инвариант)
        for c in self._categories.values():
            if c.name.value == category.name.value:
                raise InvalidTransactionException(f"Категория с именем '{category.name.value}' уже существует")
        self._categories[category.id] = category

    def get_category(self, category_id: str) -> Category:
        if category_id not in self._categories:
            raise CategoryNotFoundException(f"Категория {category_id} не найдена")
        return self._categories[category_id]

    # --- Управление лимитами ---
    def set_limit(self, category_id: str, limit_amount: Money, period: DateRange):
        if self._is_archived:
            raise BudgetAlreadyArchivedException("Нельзя изменять архивный бюджет")
        if category_id not in self._categories:
            raise CategoryNotFoundException(f"Категория {category_id} не найдена")
        # Удаляем старый лимит на эту же категорию с пересекающимся периодом
        self._limits = [l for l in self._limits if not (l.category_id == category_id and self._periods_overlap(l.period, period))]
        self._limits.append(BudgetLimit(category_id, limit_amount, period))

    @staticmethod
    def _periods_overlap(p1: DateRange, p2: DateRange) -> bool:
        return not (p1.end < p2.start or p2.end < p1.start)

    def _get_limit_for_category_at_date(self, category_id: str, dt: date) -> Optional[BudgetLimit]:
        for limit in self._limits:
            if limit.category_id == category_id and limit.period.contains(dt):
                return limit
        return None

    def _calculate_spent_for_category_in_period(self, category_id: str, period: DateRange) -> Money:
        total = Money(0, "RUB")  # Предполагаем RUB, можно брать из первого лимита
        for tx in self._transactions.values():
            if tx.category_id == category_id and tx.type == TransactionType.EXPENSE and period.contains(tx.date):
                total = total + tx.amount
        return total

    # --- Добавление транзакции с проверкой лимита ---
    def add_transaction(self, transaction: Transaction):
        if self._is_archived:
            raise BudgetAlreadyArchivedException("Нельзя изменять архивный бюджет")
        if transaction.member_id not in self._members:
            raise MemberNotFoundException(f"Член семьи {transaction.member_id} не найден")
        if transaction.category_id not in self._categories:
            raise CategoryNotFoundException(f"Категория {transaction.category_id} не найдена")

        # Проверка лимита (только для расходов)
        if transaction.type == TransactionType.EXPENSE:
            limit = self._get_limit_for_category_at_date(transaction.category_id, transaction.date)
            if limit:
                spent_before = self._calculate_spent_for_category_in_period(transaction.category_id, limit.period)
                if (spent_before + transaction.amount).amount > limit.limit_amount.amount:
                    exceeded = (spent_before + transaction.amount) - limit.limit_amount
                    self._events.append(LimitExceededEvent(
                        self.id, self._categories[transaction.category_id].name.value,
                        limit.limit_amount, spent_before + transaction.amount, exceeded
                    ))
                    # По бизнес‑правилам можно запретить транзакцию или разрешить с событием.
                    # Для демонстрации запрещаем:
                    raise LimitExceededException(
                        f"Превышен лимит для категории {self._categories[transaction.category_id].name.value}. "
                        f"Лимит: {limit.limit_amount.amount}, превышение: {exceeded.amount}"
                    )

        self._transactions[transaction.id] = transaction
        self._events.append(TransactionAddedEvent(
            self.id, transaction.id, transaction.amount,
            self._categories[transaction.category_id].name.value,
            self._members[transaction.member_id].name.value,
            transaction.type == TransactionType.EXPENSE
        ))

    # --- Архивация бюджета ---
    def archive(self):
        if not self._is_archived:
            self._is_archived = True
            self._events.append(BudgetArchivedEvent(self.id))

    # --- Сбор событий ---
    def pull_events(self) -> List[DomainEvent]:
        events = self._events.copy()
        self._events.clear()
        return events

    # --- Вспомогательные методы для отчётов ---
    def get_transactions(self) -> List[Transaction]:
        return list(self._transactions.values())

    def get_members(self) -> List[FamilyMember]:
        return list(self._members.values())

    def get_categories(self) -> List[Category]:
        return list(self._categories.values())