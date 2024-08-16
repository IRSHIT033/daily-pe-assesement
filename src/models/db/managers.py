import datetime
from uuid import UUID, uuid4

import sqlalchemy
from sqlalchemy.orm import relationship as sqlalchemy_relationship, Mapped as SQLAlchemyMapped, mapped_column as sqlalchemy_mapped_column 
from sqlalchemy.sql import functions as sqlalchemy_functions

from src.repository.table import Base


class Manager(Base):  # type: ignore
    __tablename__ = "managers"

    manager_id: SQLAlchemyMapped[UUID] = sqlalchemy_mapped_column(primary_key=True)
    
    job_name: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(
        sqlalchemy.String(length=64), nullable=False, unique=True
    )

    manager_name: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(
        sqlalchemy.String(length=64), nullable=False, unique=True
    )

    is_active: SQLAlchemyMapped[bool] = sqlalchemy_mapped_column(sqlalchemy.Boolean, nullable=False, default=True)
    
    created_at: SQLAlchemyMapped[datetime.datetime] = sqlalchemy_mapped_column(
        sqlalchemy.DateTime(timezone=True), nullable=False, server_default=sqlalchemy_functions.now()
    )
    updated_at: SQLAlchemyMapped[datetime.datetime] = sqlalchemy_mapped_column(
        sqlalchemy.DateTime(timezone=True),
        nullable=True,
        server_onupdate=sqlalchemy.schema.FetchedValue(for_update=True),
    )

    users = sqlalchemy_relationship("User")

    __mapper_args__ = {"eager_defaults": True}

    def __init__(self, **kwargs):
        if 'id' not in kwargs:
            kwargs['manager_id'] = uuid4()
        super().__init__(**kwargs)