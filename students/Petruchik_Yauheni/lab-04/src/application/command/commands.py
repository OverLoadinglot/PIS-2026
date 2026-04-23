from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class CreateBudgetCommand:
    budget_id: str
    name: str

    def __post_init__(self):
        if not self.budget_id or not self.budget_id.strip():
            raise ValueError("ID бюджета не может быть пустым")
        if not self.name or len(self.name.strip()) < 3:
            raise ValueError("Название бюджета должно содержать минимум 3 символа")


@dataclass(frozen=True)
class AddMemberCommand:
    budget_id: str
    member_id: str
    member_name: str

    def __post_init__(self):
        if not self.budget_id or not self.member_id:
            raise ValueError("ID бюджета и члена семьи обязательны")
        if not self.member_name or len(self.member_name.strip()) < 2:
            raise ValueError("Имя члена семьи должно содержать минимум 2 символа")


@dataclass(frozen=True)
class AddCategoryCommand:
    budget_id: str
    category_id: str
    category_name: str

    def __post_init__(self):
        if not self.budget_id or not self.category_id:
            raise ValueError("ID бюджета и категории обязательны")
        if not self.category_name or len(self.category_name.strip()) < 2:
            raise ValueError("Название категории должно содержать минимум 2 символа")


@dataclass(frozen=True)
class SetLimitCommand:
    budget_id: str
    category_id: str
    amount: float
    currency: str
    start_date: date
    end_date: date

    def __post_init__(self):
        if not self.budget_id or not self.category_id:
            raise ValueError("ID бюджета и категории обязательны")
        if self.amount < 0:
            raise ValueError("Лимит не может быть отрицательным")
        if self.start_date > self.end_date:
            raise ValueError("Дата начала не может быть позже даты окончания")
        if not self.currency or not self.currency.strip():
            raise ValueError("Валюта не может быть пустой")


@dataclass(frozen=True)
class AddTransactionCommand:
    budget_id: str
    transaction_id: str
    amount: float
    currency: str
    type: str
    category_id: str
    member_id: str
    date: date
    description: str = ""

    def __post_init__(self):
        if not self.budget_id or not self.transaction_id:
            raise ValueError("ID бюджета и транзакции обязательны")
        if self.amount < 0:
            raise ValueError("Сумма транзакции не может быть отрицательной")
        if self.type not in ("income", "expense"):
            raise ValueError("Тип транзакции должен быть income или expense")
        if not self.category_id or not self.member_id:
            raise ValueError("Категория и член семьи обязательны")
        if not self.currency or not self.currency.strip():
            raise ValueError("Валюта не может быть пустой")
