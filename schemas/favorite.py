from pydantic import BaseModel, Field

class FavoriteCheckResponse(BaseModel):
    is_favorited: bool = Field(..., alias = "isFavorited", description="是否已收藏")

# 添加收藏的请求体参数对象
class FavoriteAddRequest(BaseModel):
    news_id: int = Field(..., alias="newsId", description="新闻ID")
    