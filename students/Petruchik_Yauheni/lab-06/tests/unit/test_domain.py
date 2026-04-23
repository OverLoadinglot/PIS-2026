import pytest
from datetime import date

from src.domain.models.budget import FamilyBudget, Money, Transaction
from src.domain.models.exceptions import BudgetAlreadyArchivedException, MemberNotFoundException, CategoryNotFoundException


def test_add_transaction_requires_member_and_category():
    budget = FamilyBudget('b1', 'Про рубли', {}, {})
    budget.add_member('m1', 'Папа')
    budget.add_category('c1', 'Продукты')
    transaction = Transaction('t1', Money(100, 'RUB'), 'expense', 'c1', 'm1', date.today(), 'Супермаркет')

    budget.add_transaction(transaction)

    assert len(budget.get_transactions()) == 1


def test_add_transaction_missing_member_raises():
    budget = FamilyBudget('b1', 'Про рубли', {}, {'c1': 'Продукты'})
    transaction = Transaction('t1', Money(100, 'RUB'), 'expense', 'c1', 'm1', date.today(), 'Супермаркет')

    with pytest.raises(MemberNotFoundException):
        budget.add_transaction(transaction)


def test_archive_budget_blocks_changes():
    budget = FamilyBudget('b1', 'Про рубли', {'m1': 'Папа'}, {'c1': 'Продукты'})
    budget.is_archived = True
    transaction = Transaction('t1', Money(50, 'RUB'), 'expense', 'c1', 'm1', date.today(), 'Пирожки')

    with pytest.raises(BudgetAlreadyArchivedException):
        budget.add_transaction(transaction)
