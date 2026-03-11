from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

from app.core.config import settings
from app.db.session import Base
from app.models.task import Task

# Loads Alembic config and sets up logging - don't modify
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Connects to db as migration user
assert settings.MIGRATION_DATABASE_URL, (
    "MIGRATION_DATABASE_URL must be set. "
    "Migrations should never run as the runtime user."
)
db_url = settings.MIGRATION_DATABASE_URL
# Tells where db is, overrides placeholder in alembic.ini
config.set_main_option("sqlalchemy.url", db_url)
# Tells Alembic what schema looks like
target_metadata = Base.metadata

# Runs migrations without a live DB connection using a static URL - don't modify
def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"}
    )
    with context.begin_transaction():
        context.run_migrations()
        
# Runs migrations using a live DB connection and connection pool - don't modify
def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

# Entry point: uses offline or online migration mode - don't modify
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()