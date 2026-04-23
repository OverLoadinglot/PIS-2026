from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_engine(url: str = 'sqlite:///:memory:'):
    return create_engine(url, echo=False, future=True)


def get_session(engine):
    return sessionmaker(bind=engine)
