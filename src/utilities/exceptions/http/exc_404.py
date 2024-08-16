"""
The HTTP 404 Not Found response status code indicates that the server cannot find the requested resource.
"""

from typing import List
import fastapi
from uuid import UUID 
from src.utilities.messages.exceptions.http.exc_details import (
    http_404_user_not_found,
    http_404_manager_not_found,
    http_404_users_not_found

)


async def http_404_exc_user_not_found() -> Exception:
    return fastapi.HTTPException(
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
        detail=http_404_user_not_found(),
    )

async def http_404_exc_manager_not_found() -> Exception:
    return fastapi.HTTPException(
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
        detail=http_404_manager_not_found(),
    )

async def http_404_exc_users_not_found(user_ids:List[UUID]) -> Exception:
    return fastapi.HTTPException(
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
        detail=http_404_users_not_found(missing_ids=user_ids),
    )






