from src.application.command.commands import AddTransactionCommand
from src.application.ports.repository import BudgetRepository
from src.application.ports.event_publisher import EventPublisher
from src.domain import Money, Transaction, TransactionType


class AddTransactionHandler:
    def __init__(self, repository: BudgetRepository, event_publisher: EventPublisher):
        self.repository = repository
        self.event_publisher = event_publisher

    def handle(self, command: AddTransactionCommand) -> None:
        budget = self.repository.get_by_id(command.budget_id)
        if budget is None:
            raise ValueError(f"Бюджет с ID {command.budget_id} не найден")

        transaction = Transaction(
            command.transaction_id,
            Money(command.amount, command.currency),
            command.type,
            command.category_id,
            command.member_id,
            command.date,
            command.description,
        )

        budget.add_transaction(transaction)
        self.repository.save(budget)

        events = budget.pull_events()
        self.event_publisher.publish_all(events)
