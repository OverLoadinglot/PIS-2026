from dataclasses import dataclass
from enum import Enum
from datetime import date
from typing import Optional

class TransactionType(Enum):
    INCOME = "income"
    EXPENSE = "expense"

@dataclass(frozen=True)
class Money:
    amount: float
    currency: str = "RUB"

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Сумма не может быть отрицательной")
        if not self.currency:
            raise ValueError("Валюта не может быть пустой")

    def __add__(self, other: 'Money') -> 'Money':
        if self.currency != other.currency:
            raise ValueError("Нельзя складывать деньги в разных валютах")
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other: 'Money') -> 'Money':
        if self.currency != other.currency:
            raise ValueError("Нельзя вычитать деньги в разных валютах")
        return Money(self.amount - other.amount, self.currency)

@dataclass(frozen=True)
class CategoryName:
    value: str

    def __post_init__(self):
        if not self.value or len(self.value.strip()) < 2:
            raise ValueError("Название категории должно содержать минимум 2 символа")

@dataclass(frozen=True)
class MemberName:
    value: str

    def __post_init__(self):
        if not self.value or len(self.value.strip()) < 1:
            raise ValueError("Имя члена семьи не может быть пустым")

@dataclass(frozen=True)
class DateRange:
    start: date
    end: date

    def __post_init__(self):
        if self.start > self.end:
            raise ValueError("Дата начала не может быть позже даты окончания")

    def contains(self, d: date) -> bool:
        return self.start <= d <= self.end

@dataclass(frozen=True)
class Percentage:
    value: float

    def __post_init__(self):
        if not (0 <= self.value <= 100):
            raise ValueError("Процент должен быть от 0 до 100")