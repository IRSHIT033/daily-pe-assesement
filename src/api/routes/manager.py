



import fastapi
from src.api.dependencies.repository import get_repository
from src.repository.crud.manager import ManagerRepository
from loguru import logger

router = fastapi.APIRouter(prefix="/managers", tags=["managers"])


      