

from src.repository.crud.base import BaseRepository
from src.models.db.managers import Manager

class ManagerRepository(BaseRepository):
      async def seed_manager_data(self) :
            new_manager= Manager(job_name="Software",manager_name="Abhirup Ghosh")
            self.async_session.add(instance=new_manager)
            await self.async_session.commit()
            await self.async_session.refresh(instance=new_manager)