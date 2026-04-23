import os
import tempfile

from sqlalchemy import create_engine
from infrastructure.adapter.out_bound.budget_repository import BudgetRepositoryImpl
from infrastructure.config.database import get_database_url


def test_budget_repository_save_and_get_by_id():
    engine = create_engine('sqlite:///:memory:', echo=False, future=True)
    repository = BudgetRepositoryImpl(engine)
    repository.create_tables()

    budget = {'budget_id': 'b49', 'name': 'Семейный бюджет Про рубли', 'is_archived': False}
    repository.save(budget)

    loaded = repository.get_by_id('b49')
    assert loaded is not None
    assert loaded.budget_id == 'b49'
    assert loaded.name == 'Семейный бюджет Про рубли'
    assert loaded.is_archived is False
