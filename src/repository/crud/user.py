from uuid import UUID
import typing
from src.models.db.users import User
from src.models.db.managers import Manager
from src.repository.crud.base import BaseRepository
from src.models.schema.users import CreateUser,GetUsersRequestBody
from sqlalchemy.sql import functions as sqlalchemy_functions
import sqlalchemy
from src.utilities.exceptions.database import EntityAlreadyExists, EntityDoesNotExist
from sqlalchemy.sql import or_

from src.models.schema.users import UserResponse

class UserRepository(BaseRepository):
    # create user 
    async def create_user(self, user_create: CreateUser) -> User:
        new_user = User(full_name=user_create.full_name,pan_num=user_create.pan_num,mob_num=user_create.mob_num,manager_id=user_create.manager_id)
    
        self.async_session.add(instance=new_user)
        await self.async_session.commit()
        await self.async_session.refresh(instance=new_user)

        return new_user
    
    # get all users
    async def get_all_users(self) -> list[UserResponse]:
        stmt = sqlalchemy.select(User)
        query = await self.async_session.execute(statement=stmt)
        return query.scalars().all()
    
    # get user with mob num
    async def get_user_by_mob_num(self, mob_num:str) -> UserResponse :
        stmt = sqlalchemy.select(User).where(User.mob_num == mob_num)
        query = await self.async_session.execute(statement=stmt)
        
        return query.scalars().all()
    
    # get user by user id
    async def get_user_by_user_id(self, user_id:UUID) -> UserResponse :

        stmt = sqlalchemy.select(User).where(User.user_id==user_id)
        query = await self.async_session.execute(statement=stmt)
        
        return query.scalars().all()
    
    async def get_users_by_manager_id(self, manager_id:UUID)-> list[UserResponse]:
        stmt = sqlalchemy.select(User).join(Manager,Manager.manager_id==User.manager_id).where(User.manager_id==manager_id)
        query = await self.async_session.execute(statement=stmt)
        
        return query.scalars().all()
    
    async def delete_user(self,user_id:str|None=None,mob_num:str|None=None):
        if user_id is not None:
              stmt = sqlalchemy.delete(User).where(User.user_id==user_id)
              query= await self.async_session.execute(statement=stmt)
              if query.rowcount == 0:
                raise 
              await self.async_session.commit()

        elif mob_num is not None: 
              stmt = sqlalchemy.delete(User).where(User.mob_num==mob_num)
              query=await self.async_session.execute(statement=stmt)
              if query.rowcount == 0:
                raise EntityDoesNotExist("User not found against mob_num")
              await self.async_session.commit()

        return { "message": "user deleted successfully" }    

                


        
    

    


     

   