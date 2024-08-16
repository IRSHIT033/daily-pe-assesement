from typing import Union,Optional
import fastapi
import pydantic

from src.api.dependencies.repository import get_repository
from src.models.schema.users import CreateUser,GetUsersRequestBody, UserResponse
from src.repository.crud.user import UserRepository
from src.repository.crud.user import User
from loguru import logger
# from src.utilities.exceptions.database import EntityAlreadyExists, EntityDoesNotExist
# from src.utilities.exceptions.http.exc_404 import (
#     http_404_exc_email_not_found_request,
#     http_404_exc_id_not_found_request,
#     http_404_exc_username_not_found_request,
# )

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

    new_user = await user_repo.create_user(create_user)
   
    return new_user


@router.post(
    "/get_users",
    name="users:get",
    response_model=list[UserResponse],
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def get_users(
    get_user: GetUsersRequestBody,
    user_repo:UserRepository  = fastapi.Depends(get_repository(repo_type=UserRepository)),
) -> Union[list[UserResponse],Optional[UserResponse]] :
    
    if get_user.mob_num is not None:
        return await user_repo.get_user_by_mob_num(get_user.mob_num)
    
    if get_user.user_id is not None:
         return await user_repo.get_user_by_user_id(get_user.user_id)
         
    if get_user.manager_id is not None:
        return await user_repo.get_users_by_manager_id()

    else :
        return await user_repo.get_all_users()
        