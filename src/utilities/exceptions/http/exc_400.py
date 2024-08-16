"""
The HyperText Transfer Protocol (HTTP) 400 Bad Request response status code indicates that the server
cannot or will not process the request due to something that is perceivedto be a client error
(for example, malformed request syntax, invalid request message framing, or deceptive request routing).
"""

import fastapi
from typing import List


from src.utilities.messages.exceptions.http.exc_details import (
    http_400_user_ids_not_Provided,
    http_400_bulk_update_extra_keys,
   
)


async def http_400_exc_user_ids_not_provided() -> Exception:
    return fastapi.HTTPException(
        status_code=fastapi.status.HTTP_400_BAD_REQUEST,
        detail=http_400_user_ids_not_Provided(),
    )

async def http_400_exc_bulk_update_extra_keys(extra_keys:List[str]) -> Exception:
    return fastapi.HTTPException(
        status_code=fastapi.status.HTTP_400_BAD_REQUEST,
        detail=http_400_bulk_update_extra_keys(extra_keys=extra_keys),
    )