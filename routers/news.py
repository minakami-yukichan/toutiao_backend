from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from crud.news import get_category

# 创建apirouter实例
# prefix 路由前缀， tags 路由标签
router = APIRouter(prefix="/api/news", tags=["news"])


# 接口类实现
# 1. 模块化路由 -> api 接口规范文档
# 2. 定义模型类 -> 数据库表结构 -> ORM模型类
# 3. 在crud文件夹里创建文件，封装操作数据库的方法
# 4. 在路由处理函数里调用 crud 封装好的方法 响应结果

@router.get("/categories")
async def get_news_categories(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
    获取新闻分类列表
    """
    # 先获取数据库中的新闻分类数据 -> 定义模型类 -> 封装获取数据方法
    categories = await get_category(db, skip = skip, limit = limit)

    return {
        "code": 200,
        "message": "获取新闻分类成功",
        "data": categories
    }