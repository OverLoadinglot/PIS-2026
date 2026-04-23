from logging.config import fileConfig
import os

from sqlalchemy import engine_from_config, pool
from alembic import context

config = context.config
fileConfig(config.config_file_name)

target_metadata = None


def get_url():
    return os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/budgetdb')

config.set_main_option('sqlalchemy.url', get_url())

with context.begin_transaction():
    context.run_migrations()
