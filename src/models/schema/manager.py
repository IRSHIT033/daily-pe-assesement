from uuid import UUID

from src.models.schema.base import BaseSchemaModel

class Manager(BaseSchemaModel):
    job_name: str
    manager_id: UUID | None = None