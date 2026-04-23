from src.cqrs.projection.budget_projection import BudgetProjection


def test_budget_projection_increments_transactions_count():
    projection = BudgetProjection()
    event = {
        'budget_id': 'b49',
        'budget_name': 'Про рубли',
        'members_count': 3,
        'categories_count': 5,
    }

    projection.apply_transaction_added(event)
    summary = projection.get_summary('b49')

    assert summary is not None
    assert summary.transactions_count == 1
    assert summary.budget_id == 'b49'
    assert summary.name == 'Про рубли'
