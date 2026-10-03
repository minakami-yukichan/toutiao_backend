from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from models.users import User
from utils.auth import get_current_user
from utils.response import success_response
from crud import favorite
from schemas.favorite import FavoriteCheckResponse, FavoriteAddRequest

router = APIRouter(prefix="/favorite", tags=["favorite"])

@router.get("/check")
async def check_favorite(news_id: int = Query(..., alias="newsId"), user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    is_favorited = await favorite.is_news_favorite(db, user.id, news_id)
    return success_response(message="检查收藏状态成功", data=FavoriteCheckResponse(isFavorited=is_favorited))

@router.post("/add")
async def add_favorite(data: FavoriteAddRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await favorite.add_favorite(db, user.id, data.news_id)
    return success_response(message="添加收藏成功", data=result)

@router.delete("/remove")
async def remove_favorite(news_id: int = Query(..., alias="newsId"), user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await favorite.remove_favorite(db, user.id, news_id)
    if not result:
        raise HTTPException(status_code=404, detail="收藏记录不存在")
    return success_response(message="取消收藏成功")