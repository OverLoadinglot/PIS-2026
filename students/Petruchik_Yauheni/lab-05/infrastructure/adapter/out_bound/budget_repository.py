from sqlalchemy import Column, String, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class BudgetOrm(Base):
    __tablename__ = 'budgets'
    budget_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    is_archived = Column(Boolean, nullable=False, default=False)

class BudgetRepositoryImpl:
    def __init__(self, engine):
        self.engine = engine
        self.Session = sessionmaker(bind=engine)

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def save(self, budget):
        with self.Session() as session:
            entity = session.get(BudgetOrm, budget['budget_id'])
            if entity is None:
                entity = BudgetOrm(
                    budget_id=budget['budget_id'],
                    name=budget['name'],
                    is_archived=budget.get('is_archived', False)
                )
                session.add(entity)
            else:
                entity.name = budget['name']
                entity.is_archived = budget.get('is_archived', entity.is_archived)
            session.commit()

    def get_by_id(self, budget_id):
        with self.Session() as session:
            return session.get(BudgetOrm, budget_id)
