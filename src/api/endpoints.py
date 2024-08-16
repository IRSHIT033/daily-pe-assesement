import fastapi

from src.api.routes.user import router as user_router
from src.api.routes.manager import router as manager_router

router = fastapi.APIRouter()
router.include_router(router=user_router)
router.include_router(router=manager_router)
