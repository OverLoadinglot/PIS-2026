import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_database_url():
    return os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/budgetdb')


def get_engine():
    return create_engine(get_database_url(), echo=False, future=True)


def get_session(engine):
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)()
