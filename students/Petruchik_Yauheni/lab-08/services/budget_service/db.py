# Заглушка для отдельной БД Budget Service

class BudgetDatabase:
    def __init__(self):
        self.budgets = {}

    def save_budget(self, budget):
        self.budgets[budget['budget_id']] = budget

    def get_budget(self, budget_id):
        return self.budgets.get(budget_id)
