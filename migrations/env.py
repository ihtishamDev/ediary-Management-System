from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from sqlalchemy import create_engine, inspect
from alembic import context

# Alembic Config object
config = context.config

# Logging config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import your Base from models
from app.db import Base
from app import models

target_metadata = models.Base.metadata

   # <-- ye zaroori hai

# Optional: if you want to inspect DB columns (debugging)
engine = create_engine("sqlite:///C:/Users/dell/Desktop/ediary-project/data.db")
insp = inspect(engine)
for col in insp.get_columns("users"):
    print(col["name"], col["type"])


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata   # <-- yaha bhi Base.metadata use ho raha hai
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()    
else:
    run_migrations_online()

