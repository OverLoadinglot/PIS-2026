from src.application.command.commands import (
    AddCategoryCommand,
    AddMemberCommand,
    AddTransactionCommand,
    CreateBudgetCommand,
    SetLimitCommand,
)
from src.application.command.handlers.add_category_handler import AddCategoryHandler
from src.application.command.handlers.add_member_handler import AddMemberHandler
from src.application.command.handlers.add_transaction_handler import AddTransactionHandler
from src.application.command.handlers.create_budget_handler import CreateBudgetHandler
from src.application.command.handlers.set_limit_handler import SetLimitHandler
from src.application.query.handlers.get_budget_handler import GetBudgetByIdHandler
from src.application.query.queries import GetBudgetByIdQuery
from src.application.ports.event_publisher import EventPublisher
from src.application.ports.repository import BudgetRepository


class BudgetApplicationService:
    def __init__(self, repository: BudgetRepository, event_publisher: EventPublisher):
        self.create_budget_handler = CreateBudgetHandler(repository)
        self.add_member_handler = AddMemberHandler(repository)
        self.add_category_handler = AddCategoryHandler(repository)
        self.set_limit_handler = SetLimitHandler(repository)
        self.add_transaction_handler = AddTransactionHandler(repository, event_publisher)
        self.get_budget_handler = GetBudgetByIdHandler(repository)

    def create_budget(self, command: CreateBudgetCommand) -> str:
        return self.create_budget_handler.handle(command)

    def add_member(self, command: AddMemberCommand) -> None:
        self.add_member_handler.handle(command)

    def add_category(self, command: AddCategoryCommand) -> None:
        self.add_category_handler.handle(command)

    def set_limit(self, command: SetLimitCommand) -> None:
        self.set_limit_handler.handle(command)

    def add_transaction(self, command: AddTransactionCommand) -> None:
        self.add_transaction_handler.handle(command)

    def get_budget(self, query: GetBudgetByIdQuery):
        return self.get_budget_handler.handle(query)
