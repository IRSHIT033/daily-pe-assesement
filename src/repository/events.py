import fastapi
import loguru
from sqlalchemy import event
from sqlalchemy.dialects.postgresql.asyncpg import AsyncAdapt_asyncpg_connection
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSessionTransaction
from sqlalchemy.pool.base import _ConnectionRecord

from src.models.db.managers import Manager
from src.repository.database import async_db
from src.repository.table import Base


@event.listens_for(target=async_db.async_engine.sync_engine, identifier="connect")
def inspect_db_server_on_connection(
    db_api_connection: AsyncAdapt_asyncpg_connection, connection_record: _ConnectionRecord
) -> None:
    loguru.logger.info(f"New DB API Connection ---\n {db_api_connection}")
    loguru.logger.info(f"Connection Record ---\n {connection_record}")


@event.listens_for(target=async_db.async_engine.sync_engine, identifier="close")
def inspect_db_server_on_close(
    db_api_connection: AsyncAdapt_asyncpg_connection, connection_record: _ConnectionRecord
) -> None:
    loguru.logger.info(f"Closing DB API Connection ---\n {db_api_connection}")
    loguru.logger.info(f"Closed Connection Record ---\n {connection_record}")


async def initialize_db_tables(connection: AsyncConnection) -> None:
    loguru.logger.info("Database Table Creation --- Initializing . . .")

    await connection.run_sync(Base.metadata.drop_all)
    await connection.run_sync(Base.metadata.create_all)

    loguru.logger.info("Database Table Creation --- Successfully Initialized!")



async def initialize_db_connection(backend_app: fastapi.FastAPI) -> None:
    loguru.logger.info("Database Connection --- Establishing . . .")

    backend_app.state.db = async_db
    
    async with backend_app.state.db.async_engine.begin() as connection:
        await initialize_db_tables(connection=connection)

    loguru.logger.info("Database Connection --- Successfully Established!")


async def seed_manager_data(backend_app: fastapi.FastAPI) -> None:
    loguru.logger.info("Manager data seeding started . . .")
    
    manager_one= Manager(job_name="Software",manager_name="Abhirup Ghosh")
    backend_app.state.session= async_db.async_session
    backend_app.state.session.add(instance=manager_one)
    await backend_app.state.session.commit()
    await backend_app.state.session.refresh(instance=manager_one)

    manager_two= Manager(job_name="Management",manager_name="Aritra Roy")
    backend_app.state.session= async_db.async_session
    backend_app.state.session.add(instance=manager_two)
    await backend_app.state.session.commit()
    await backend_app.state.session.refresh(instance=manager_two)

    loguru.logger.info("Seeding --- Successfully Completed!")    



async def dispose_db_connection(backend_app: fastapi.FastAPI) -> None:
    loguru.logger.info("Database Connection --- Disposing . . .")

    await backend_app.state.db.async_engine.dispose()

    loguru.logger.info("Database Connection --- Successfully Disposed!")