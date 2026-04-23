from src.application.command.commands import AddTransactionCommand
from src.application.command.handlers.add_transaction_handler import AddTransactionHandler
from src.application.query.handlers.get_budget_handler import GetBudgetByIdHandler
from src.application.query.queries import GetBudgetByIdQuery
from src.application.ports.event_publisher import EventPublisher
from src.application.ports.repository import BudgetRepository


class BudgetApplicationService:
    def __init__(self, repository: BudgetRepository, event_publisher: EventPublisher):
        self.add_transaction_handler = AddTransactionHandler(repository, event_publisher)
        self.get_budget_handler = GetBudgetByIdHandler(repository)

    def add_transaction(self, command: AddTransactionCommand) -> None:
        self.add_transaction_handler.handle(command)

    def get_budget(self, query: GetBudgetByIdQuery):
        return self.get_budget_handler.handle(query)
