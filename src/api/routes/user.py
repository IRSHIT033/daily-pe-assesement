from datetime import datetime,timezone
from typing import Union,Optional
import fastapi

from src.api.dependencies.repository import get_repository
from src.models.schema.users import CreateUser,GetUsersRequestBody, UserResponse, DeleteUserRequestBody, DeleteUserResponse,BulkUpdateUserRequestBody, BulkUpdateUserResponse
from src.repository.crud.user import UserRepository
from src.models.db.users import User

from src.utilities.exceptions.http.exc_404 import (
    http_404_exc_user_not_found,
    http_404_exc_users_not_found,
    http_404_exc_manager_not_found
)
from src.utilities.exceptions.http.exc_400 import (
    http_400_exc_user_ids_not_provided,
    http_400_exc_bulk_update_extra_keys
)

router = fastapi.APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/create_user",
    name="users:create",
    response_model=UserResponse,
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def create_user(
    create_user: CreateUser,
    user_repo:UserRepository  = fastapi.Depends(get_repository(repo_type=UserRepository)),
) -> UserResponse:
    # check if manager exists or not
    manager_exists=await user_repo.get_manager_by_id(manager_id=create_user.manager_id)
    if not manager_exists:
        raise await http_404_exc_manager_not_found() 
    #create user
    new_user = await user_repo.create_user(create_user)
   
    return new_user


@router.post(
    "/get_users",
    name="users:get",
    response_model=list[UserResponse],
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_users(
    get_user: GetUsersRequestBody,
    user_repo:UserRepository  = fastapi.Depends(get_repository(repo_type=UserRepository)),
) -> Union[list[UserResponse],Optional[UserResponse]]:
    # get user matching mob_num
    if get_user.mob_num is not None:
        return await user_repo.get_user_by_mob_num(get_user.mob_num)
    # get user matching user_id
    if get_user.user_id is not None:
        return await user_repo.get_user_by_user_id(get_user.user_id)
    # get users under manager      
    if get_user.manager_id is not None:
        return await user_repo.get_users_under_manager_id(get_user.manager_id)
    #get all users
    else :
        return await user_repo.get_all_users()


@router.post(
    "/delete_user",
    name="user:delete",
    response_model=DeleteUserResponse,
    status_code=fastapi.status.HTTP_202_ACCEPTED,
) 
async def delete_user(
    del_user: DeleteUserRequestBody ,
    user_repo:UserRepository  = fastapi.Depends(get_repository(repo_type=UserRepository)),
):
   # delete user
   try: 
       await user_repo.delete_user(user_id=del_user.user_id,mob_num=del_user.mob_num)
   except :
       # raise exception if user not found 
       raise await http_404_exc_user_not_found()
   
   return { "message": "user deleted successfully" }  


@router.post(
    "/update_user",
    name="user:update",
    response_model=BulkUpdateUserResponse,
    status_code=fastapi.status.HTTP_202_ACCEPTED,
)
async def update_user(
    update_info:BulkUpdateUserRequestBody,
    user_repo:UserRepository  = fastapi.Depends(get_repository(repo_type=UserRepository)),
):
    user_ids = update_info.user_ids
    update_data= update_info.update_data.dict(exclude_unset=True)
   
    if not user_ids:
        raise await http_400_exc_user_ids_not_provided()
    
    # get all users with with matching user_ids
    users= await user_repo.get_all_users(user_ids=user_ids)

    # Check if all user_ids exist in the database
    existing_user_ids = [user.user_id for user in users]
    missing_user_ids = set(user_ids) - set(existing_user_ids)

    if missing_user_ids:
       raise await http_404_exc_users_not_found(user_ids=list(missing_user_ids))
    
    # Check if it's a bulk update for manager_id only
    if len(user_ids) > 1 and ('full_name' in update_data or 'mob_num' in update_data or 'pan_num' in update_data):
       extra_keys = [key for key in update_data.keys() if key != 'manager_id']
       raise await http_400_exc_bulk_update_extra_keys(extra_keys=extra_keys)
    
    if "manager_id" in update_data:
        manager_id= update_data.get('manager_id')
        # Validate manager existence
        manager=await user_repo.get_manager_by_id(manager_id=manager_id)
        if not manager:
            raise await http_404_exc_manager_not_found()
        
        # For each user, update manager_id or create a new entry if they already have a manager
        for user in users:  
            if user.manager_id:
                user.is_active=False
                new_user=User(full_name=user.full_name,pan_num=user.pan_num,mob_num=user.mob_num,manager_id=manager_id,updated_at=datetime.now(timezone.utc))
                user_repo.async_session.add(new_user) 
            else:
                user.manager_id=manager_id
                
    else:
        # For individual updates of other fields
        for user in users:
            for key, value in update_data.items():
               setattr(user,key,value)

    await user_repo.async_session.commit()           
            
                   
    return {"message":"User(s) updated successfully"}

                     


