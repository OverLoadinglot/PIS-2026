from abc import ABC, abstractmethod
from datetime import date
from typing import List, Callable
from .entities import Transaction
from .value_objects import DateRange, TransactionType

class Specification(ABC):
    @abstractmethod
    def is_satisfied_by(self, transaction: Transaction) -> bool:
        pass

    def __and__(self, other: 'Specification') -> 'AndSpecification':
        return AndSpecification(self, other)

    def __or__(self, other: 'Specification') -> 'OrSpecification':
        return OrSpecification(self, other)

    def __invert__(self) -> 'NotSpecification':
        return NotSpecification(self)

class AndSpecification(Specification):
    def __init__(self, left: Specification, right: Specification):
        self.left = left
        self.right = right
    def is_satisfied_by(self, transaction: Transaction) -> bool:
        return self.left.is_satisfied_by(transaction) and self.right.is_satisfied_by(transaction)

class OrSpecification(Specification):
    def __init__(self, left: Specification, right: Specification):
        self.left = left
        self.right = right
    def is_satisfied_by(self, transaction: Transaction) -> bool:
        return self.left.is_satisfied_by(transaction) or self.right.is_satisfied_by(transaction)

class NotSpecification(Specification):
    def __init__(self, spec: Specification):
        self.spec = spec
    def is_satisfied_by(self, transaction: Transaction) -> bool:
        return not self.spec.is_satisfied_by(transaction)

# Конкретные спецификации
class ByCategoryIdSpecification(Specification):
    def __init__(self, category_id: str):
        self.category_id = category_id
    def is_satisfied_by(self, transaction: Transaction) -> bool:
        return transaction.category_id == self.category_id

class ByMemberIdSpecification(Specification):
    def __init__(self, member_id: str):
        self.member_id = member_id
    def is_satisfied_by(self, transaction: Transaction) -> bool:
        return transaction.member_id == self.member_id

class ByDateRangeSpecification(Specification):
    def __init__(self, date_range: DateRange):
        self.date_range = date_range
    def is_satisfied_by(self, transaction: Transaction) -> bool:
        return self.date_range.contains(transaction.date)

class ByTypeSpecification(Specification):
    def __init__(self, tx_type: TransactionType):
        self.tx_type = tx_type
    def is_satisfied_by(self, transaction: Transaction) -> bool:
        return transaction.type == self.tx_type