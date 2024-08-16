

import datetime
from uuid import UUID
from pydantic import validator
import loguru

from src.models.schema.base import BaseSchemaModel
import re

# Regular expressions for validation
mob_num_regex = r"^(?:0|\+91)?[6-9]\d{9}$"
pan_num_regex = r"^[A-Z]{3}[PCH][A-Z][0-9]{4}[A-Z]$"


class CreateUser(BaseSchemaModel):
    full_name: str
    mob_num: str
    pan_num: str
    manager_id: UUID | None = None
    @validator('full_name')
    def validate_full_name(cls, v):
        if not v or len(v)==0:
            loguru.logger.error('full_name cannot be empty')
            raise ValueError('full_name cannot be empty')
        return v

    @validator('mob_num')
    def validate_mob_num(cls, v):
        if not re.match(mob_num_regex, v):
            loguru.logger.error('Invalid mobile number')
            raise ValueError('Invalid mobile number')
        # Remove any prefix and keep last 10 digits
        return v[-10:] 

    @validator('pan_num')
    def validate_pan_num(cls, v):
        if not re.match(pan_num_regex, v.upper()):
            loguru.logger.error('Invalid PAN number')
            raise ValueError('Invalid PAN number')
        return v.upper()

class UserResponse(BaseSchemaModel):
    full_name: str
    mob_num: str
    pan_num: str
    manager_id: UUID | None = None
    is_active: bool
    updated_at: datetime.datetime | None
    created_at: datetime.datetime 


class GetUsersRequestBody(BaseSchemaModel):
    mob_num: str | None = None
    user_id: UUID | None = None
    manager_id: UUID | None = None
    @validator('mob_num')
    def validate_mob_num(cls, v):
        if not re.match(mob_num_regex, v):
            loguru.logger.error('Invalid mobile number')
            raise ValueError('Invalid mobile number')
        # Remove any prefix and keep last 10 digits
        return v[-10:]
  