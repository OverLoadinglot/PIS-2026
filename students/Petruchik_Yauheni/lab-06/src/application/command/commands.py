from dataclasses import dataclass
from datetime import date


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
