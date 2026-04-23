import json
from sqlalchemy import Column, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class BudgetOrm(Base):
    __tablename__ = 'budgets'
    budget_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    members = Column(Text, nullable=False, default='{}')
    categories = Column(Text, nullable=False, default='{}')
    transactions = Column(Text, nullable=False, default='{}')
    is_archived = Column(String, nullable=False, default='false')

class BudgetRepositoryImpl:
    def __init__(self, engine=None):
        self.engine = engine or create_engine('sqlite:///:memory:', future=True)
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def save(self, budget):
        with self.Session() as session:
            entity = session.get(BudgetOrm, budget.id)
            payload = {
                'budget_id': budget.id,
                'name': budget.name,
                'members': json.dumps(budget.members),
                'categories': json.dumps(budget.categories),
                'transactions': json.dumps({tid: {
                    'id': tx.id,
                    'amount': tx.amount.amount,
                    'currency': tx.amount.currency,
                    'type': tx.type,
                    'category_id': tx.category_id,
                    'member_id': tx.member_id,
                    'date': tx.date.isoformat(),
                    'description': tx.description,
                } for tid, tx in budget.transactions.items()}),
                'is_archived': 'true' if budget.is_archived else 'false',
            }
            if entity is None:
                entity = BudgetOrm(**payload)
                session.add(entity)
            else:
                for key, value in payload.items():
                    setattr(entity, key, value)
            session.commit()

    def get_by_id(self, budget_id):
        with self.Session() as session:
            entity = session.get(BudgetOrm, budget_id)
            if entity is None:
                return None
            return entity
