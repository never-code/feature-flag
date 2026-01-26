import sys
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# ---- FIX PATHS ----
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(project_dir)   # Now Alembic can see the app package

# ---- IMPORT BASE + MODELS ----
from app.db.database import Base
from app.models import feature_flag, evaluation  # IMPORTANT: force model loading!


# ---- METADATA ----
target_metadata = Base.metadata

# Alembic config
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Run migrations in 'online' mode
def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

def run_migrations_offline():
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
    )

    with context.begin_transaction():
        context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
