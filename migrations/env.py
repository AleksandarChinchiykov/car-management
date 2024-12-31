from __future__ import with_statement

import logging
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Alembic Config object, which provides access to the values within the .ini file.
from alembic import context

# Import your Base class and models
from database.models import Base, Car, Garage, Maintenance, CarGarage

# This is the Alembic Config object
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# Define the target metadata for Alembic to use
target_metadata = Base.metadata

# Additional configuration
def run_migrations_online():
    # Connect to the database
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    # Create a context to run migrations
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        # Run migrations
        with context.begin_transaction():
            context.run_migrations()

# Main entry point
if context.is_offline_mode():
    raise Exception("Offline mode is not supported, use online mode instead.")
else:
    run_migrations_online()
