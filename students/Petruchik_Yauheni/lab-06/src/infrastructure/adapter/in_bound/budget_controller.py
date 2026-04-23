from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

from src.application.command.commands import AddTransactionCommand
from src.application.command.handlers.add_transaction_handler import AddTransactionHandler
from src.application.ports.event_publisher import EventPublisher
from src.infrastructure.adapter.out_bound.budget_repository import BudgetRepositoryImpl
from src.infrastructure.config.database import get_engine
from src.domain.models.budget import FamilyBudget, Money, Transaction

app = FastAPI(title="Про рубли — Budget Test API")
engine = get_engine()
repository = BudgetRepositoryImpl(engine)
repository.create_tables()

class DummyPublisher(EventPublisher):
    def publish_all(self, events):
        pass

publisher = DummyPublisher()
handler = AddTransactionHandler(repository, publisher)

@app.post("/budgets/{budget_id}")
def create_budget(budget_id: str, payload: dict):
    if repository.get_by_id(budget_id) is not None:
        raise HTTPException(status_code=400, detail="Бюджет с таким ID уже существует")
    budget = FamilyBudget(budget_id, payload.get('name', ''), {}, {})
    repository.save(budget)
    return {"budget_id": budget_id, "name": budget.name}

@app.post("/budgets/{budget_id}/transactions")
def add_transaction(budget_id: str, payload: dict):
    budget = repository.get_by_id(budget_id)
    if budget is None:
        raise HTTPException(status_code=404, detail="Бюджет не найден")

    raw_date = payload.get("date")
    if isinstance(raw_date, str):
        raw_date = datetime.fromisoformat(raw_date).date()

    command = AddTransactionCommand(
        budget_id=budget_id,
        transaction_id=payload["transaction_id"],
        amount=payload["amount"],
        currency=payload.get("currency", "RUB"),
        type=payload["type"],
        category_id=payload["category_id"],
        member_id=payload["member_id"],
        date=raw_date,
        description=payload.get("description", ""),
    )
    handler.handle(command)
    return {"status": "created"}

@app.get("/budgets/{budget_id}")
def get_budget(budget_id: str):
    budget = repository.get_by_id(budget_id)
    if budget is None:
        raise HTTPException(status_code=404, detail="Бюджет не найден")
    return {"budget_id": budget.budget_id, "name": budget.name}
