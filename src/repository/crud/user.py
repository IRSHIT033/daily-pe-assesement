import datetime
from uuid import UUID
import typing
from src.models.db.users import User
from src.models.db.managers import Manager
from src.repository.crud.base import BaseRepository
from src.models.schema.users import CreateUser,UserResponse as UpdateUser
from sqlalchemy.sql import functions as sqlalchemy_functions
import sqlalchemy
from src.utilities.exceptions.database import  EntityDoesNotExist

from typing import List
from src.models.schema.users import UserResponse
from src.utilities.exceptions.http.exc_404 import http_404_exc_manager_not_found
from sqlalchemy.exc import IntegrityError
class UserRepository(BaseRepository):
    # create user 
    async def create_user(self, user_create: CreateUser) -> UserResponse:
        
        new_user = User(full_name=user_create.full_name,pan_num=user_create.pan_num,mob_num=user_create.mob_num,manager_id=user_create.manager_id)
        self.async_session.add(instance=new_user)
        await self.async_session.commit()
        await self.async_session.refresh(instance=new_user)

        return new_user
    
    # get all users
    async def get_all_users(self, user_ids: List[UUID] | None= None) -> List[UserResponse]:
        if  user_ids == None :
           stmt = sqlalchemy.select(User)
        else : 
          stmt = sqlalchemy.select(User).where(User.user_id.in_(user_ids))
       
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
    
    async def get_users_under_manager_id(self, manager_id:UUID)-> list[UserResponse]:
        stmt = sqlalchemy.select(User).join(Manager,Manager.manager_id==User.manager_id).where(User.manager_id==manager_id)
        query = await self.async_session.execute(statement=stmt)
        
        if not query:
            raise EntityDoesNotExist("Manager doesnot exists!")

        return query.scalars().all()
    
    async def get_manager_by_id(self, manager_id:UUID): 
        stmt = sqlalchemy.select(Manager).where(Manager.manager_id==manager_id)
        query = await self.async_session.execute(statement=stmt)
        # print(f"QUERY: {query.scalars().all()}")
        return query.scalars().all()
     
        
    
    async def delete_user(self,user_id:str|None=None,mob_num:str|None=None):
        if user_id is not None:
              stmt = sqlalchemy.delete(User).where(User.user_id==user_id)
              query= await self.async_session.execute(statement=stmt)
              if query.rowcount == 0:
                raise EntityDoesNotExist("User not found against user_id")
              await self.async_session.commit()

        elif mob_num is not None: 
              stmt = sqlalchemy.delete(User).where(User.mob_num==mob_num)
              query=await self.async_session.execute(statement=stmt)
              if query.rowcount == 0:
                raise EntityDoesNotExist("User not found against mob_num")
              await self.async_session.commit()


    async def update_manager(self,user:UpdateUser,manager_id:UUID):
      async with self.async_session as session:  
            if not session.is_active:
                session.add(user)
            if user.manager_id:
                user.is_active=False
                await session.commit()

                new_user=User(full_name=user.full_name,pan_num=user.pan_num,mob_num=user.mob_num,manager_id=manager_id,updated_at=datetime.utcnow())
                self.session.add(instance=new_user)
                await session.commit()
                await session.refresh(instance=new_user)
                
            else:
                user.manager_id=manager_id
                await session.commit()
            
        


        
        

        
                


        
    

    


     

   