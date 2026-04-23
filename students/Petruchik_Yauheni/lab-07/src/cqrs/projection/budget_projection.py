from src.cqrs.read_model.budget_view import BudgetSummaryView


class BudgetProjection:
    def __init__(self):
        self.views = {}

    def apply_transaction_added(self, event):
        summary = self.views.get(event['budget_id'])
        if summary is None:
            summary = BudgetSummaryView(
                budget_id=event['budget_id'],
                name=event.get('budget_name', 'Неизвестно'),
                members_count=event.get('members_count', 0),
                categories_count=event.get('categories_count', 0),
                transactions_count=0,
            )
            self.views[event['budget_id']] = summary

        summary.transactions_count += 1

    def get_summary(self, budget_id: str):
        return self.views.get(budget_id)
