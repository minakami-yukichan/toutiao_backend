from pydantic import BaseModel, Field

class FavoriteCheckResponse(BaseModel):
    is_favorited: bool = Field(..., alias = "isFavorited", description="是否已收藏")