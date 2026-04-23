from datetime import date

from sqlalchemy import create_engine

from src.domain.models.budget import FamilyBudget, Money, Transaction
from src.infrastructure.adapter.out_bound.budget_repository import BudgetRepositoryImpl


def test_repository_saves_and_loads_budget():
    engine = create_engine('sqlite:///:memory:', future=True)
    repository = BudgetRepositoryImpl(engine)
    repository.create_tables()

    budget = FamilyBudget('b1', 'Про рубли', {'m1': 'Мама'}, {'c1': 'Продукты'})
    transaction = Transaction('t1', Money(200, 'RUB'), 'expense', 'c1', 'm1', date.today(), 'Молоко')
    budget.add_transaction(transaction)
    repository.save(budget)

    loaded = repository.get_by_id('b1')
    assert loaded is not None
    assert loaded.name == 'Про рубли'
    assert 'm1' in loaded.members
    assert 'c1' in loaded.categories
