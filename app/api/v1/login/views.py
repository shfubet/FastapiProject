from app.main import app
from app.schemas.users import UserDetail
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}", response_model=UserDetail)
async def getUser():
    """
    get user
    :return:
    """
