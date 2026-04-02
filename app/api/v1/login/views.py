from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_db
from app.core.logger import logger
from app.schemas.user import UserDetail, UserList, UserListResponse, UserCreate, UserUpdate
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}", response_model=UserDetail)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    获取用户详情
    """
    logger.info_with("API: get user", "user_id", user_id)
    user = await UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user


@router.get("/", response_model=UserListResponse)
async def list_users(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: AsyncSession = Depends(get_db)
):
    """
    获取用户列表（分页）
    """
    logger.info_with("API: list users", "page", page, "page_size", page_size)
    skip = (page - 1) * page_size
    items, total = await UserService.get_users(db, skip=skip, limit=page_size)
    return UserListResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size
    )


@router.post("/", response_model=UserDetail, status_code=201)
async def create_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    创建用户
    """
    logger.info_with("API: create user", "email", user_in.email)
    try:
        return await UserService.create_user(db, user_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{user_id}", response_model=UserDetail)
async def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    更新用户
    """
    logger.info_with("API: update user", "user_id", user_id)
    try:
        user = await UserService.update_user(db, user_id, user_in)
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    删除用户（软删除）
    """
    logger.info_with("API: delete user", "user_id", user_id)
    success = await UserService.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="用户不存在")


@router.get("/search/", response_model=UserListResponse)
async def search_users(
    keyword: str = Query(..., min_length=1, description="搜索关键词"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: AsyncSession = Depends(get_db)
):
    """
    搜索用户
    """
    logger.info_with("API: search users", "keyword", keyword)
    skip = (page - 1) * page_size
    items, total = await UserService.search_users(db, keyword, skip=skip, limit=page_size)
    return UserListResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size
    )
