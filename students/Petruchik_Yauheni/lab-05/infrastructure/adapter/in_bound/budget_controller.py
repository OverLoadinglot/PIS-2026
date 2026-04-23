from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from infrastructure.adapter.out_bound.budget_repository import BudgetRepositoryImpl
from infrastructure.config.database import get_engine, get_session

app = FastAPI(title="Про рубли — Budget API")
engine = get_engine()
repository = BudgetRepositoryImpl(engine)

class BudgetCreateDto(BaseModel):
    budget_id: str
    name: str

class BudgetReadDto(BaseModel):
    budget_id: str
    name: str
    is_archived: bool

@app.on_event("startup")
def startup_event():
    with get_session(engine) as session:
        repository.create_tables()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/budgets/", response_model=BudgetReadDto)
def create_budget(body: BudgetCreateDto):
    budget = repository.get_by_id(body.budget_id)
    if budget is not None:
        raise HTTPException(status_code=400, detail="Бюджет с таким ID уже существует")

    repository.save({"budget_id": body.budget_id, "name": body.name, "is_archived": False})
    return {"budget_id": body.budget_id, "name": body.name, "is_archived": False}

@app.get("/budgets/{budget_id}", response_model=BudgetReadDto)
def get_budget(budget_id: str):
    record = repository.get_by_id(budget_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Бюджет не найден")
    return {"budget_id": record.budget_id, "name": record.name, "is_archived": record.is_archived}
