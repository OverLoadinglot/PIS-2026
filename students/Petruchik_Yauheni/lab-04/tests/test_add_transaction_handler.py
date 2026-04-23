import unittest
from unittest.mock import Mock
from datetime import date

from src.application.command.commands import AddTransactionCommand
from src.application.command.handlers.add_transaction_handler import AddTransactionHandler


class DummyBudget:
    def __init__(self, budget_id):
        self.id = budget_id
        self._events = ["DummyEvent"]
        self._transactions = {}
        self._members = {"m1": True}
        self._categories = {"c1": True}

    def add_transaction(self, transaction):
        self._transactions[transaction.id] = transaction

    def pull_events(self):
        events = self._events.copy()
        self._events.clear()
        return events


class TestAddTransactionHandler(unittest.TestCase):
    def setUp(self):
        self.mock_repo = Mock()
        self.mock_publisher = Mock()
        self.handler = AddTransactionHandler(self.mock_repo, self.mock_publisher)

    def test_handle_success(self):
        command = AddTransactionCommand(
            budget_id="b1",
            transaction_id="t1",
            amount=100.0,
            currency="RUB",
            type="expense",
            category_id="c1",
            member_id="m1",
            date=date.today(),
            description="Супермаркет"
        )
        dummy_budget = DummyBudget("b1")
        self.mock_repo.get_by_id.return_value = dummy_budget

        self.handler.handle(command)

        self.mock_repo.get_by_id.assert_called_once_with("b1")
        self.mock_repo.save.assert_called_once_with(dummy_budget)
        self.mock_publisher.publish_all.assert_called_once_with(["DummyEvent"])


if __name__ == "__main__":
    unittest.main()
