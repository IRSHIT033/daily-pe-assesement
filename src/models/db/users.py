import datetime
from uuid import UUID, uuid4

import sqlalchemy
from sqlalchemy.orm import relationship as sqlalchemy_relationship, Mapped as SQLAlchemyMapped, mapped_column as sqlalchemy_mapped_column
from sqlalchemy.sql import functions as sqlalchemy_functions

from src.repository.table import Base
from src.models.db.managers import Manager

class User(Base):  # type: ignore
    __tablename__ = "users"

    user_id: SQLAlchemyMapped[UUID] = sqlalchemy_mapped_column(primary_key=True)
    manager_id: SQLAlchemyMapped[UUID] = sqlalchemy_mapped_column(sqlalchemy.UUID(),sqlalchemy.ForeignKey(Manager.manager_id),nullable=True)
    
    full_name: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(
        sqlalchemy.String(length=64), nullable=False, unique=True
    )

    mob_num: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(sqlalchemy.String(length=10), nullable=False, unique=True)
    pan_num: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(sqlalchemy.String(length=10), nullable=False, unique=True)
    is_active: SQLAlchemyMapped[bool] = sqlalchemy_mapped_column(sqlalchemy.Boolean, nullable=False, default=True)
    
    created_at: SQLAlchemyMapped[datetime.datetime] = sqlalchemy_mapped_column(
        sqlalchemy.DateTime(timezone=True), nullable=False, server_default=sqlalchemy_functions.now()
    )
    updated_at: SQLAlchemyMapped[datetime.datetime] = sqlalchemy_mapped_column(
        sqlalchemy.DateTime(timezone=True),
        nullable=True,
        server_onupdate=sqlalchemy.schema.FetchedValue(for_update=True),
    )

    manager = sqlalchemy_relationship("Manager")

    __mapper_args__ = {"eager_defaults": True}

    def __init__(self, **kwargs):
        if 'id' not in kwargs:
            kwargs['user_id'] = uuid4()
        super().__init__(**kwargs)