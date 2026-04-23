"""
Доменная модель: Расход
"""

class Expense:
    def __init__(self, expense_id: str, amount: float, category_id: str, user_id: str, description: str):
        self.id = expense_id
        self.amount = amount
        self.category_id = category_id
        self.user_id = user_id
        self.description = description
        
        # Заглушка бизнес-логики: проверка суммы
        if self.amount <= 0:
            raise ValueError("Сумма расхода должна быть больше нуля")