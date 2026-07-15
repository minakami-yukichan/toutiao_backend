from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from crud.news import get_category, get_news_list as crud_get_news_list, get_news_count as crud_get_news_count, get_news_detail as crud_get_news_detail, increase_news_views as crud_increase_news_views, get_related_news as crud_get_related_news

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

@router.get("/list")
async def get_news_list(category_id: int = Query(..., alias="categoryId"), 
                        page: int = 1, 
                        page_size: int = Query(10, alias="pageSize", ge=1, le=100), 
                        db: AsyncSession = Depends(get_db)):
    """
    获取新闻列表
    """
    # 先获取数据库中的新闻数据 -> 定义模型类 -> 封装获取数据方法
    news_list = await crud_get_news_list(db, category_id=category_id, skip=(page - 1) * page_size, limit=page_size)
    total = await crud_get_news_count(db, category_id=category_id)
    # 跳过的 + 当前页的数量 >= 总数，说明没有更多数据了
    has_more = (page * page_size) < total
    return {
        "code": 200,
        "message": "获取新闻列表成功",
        "data": {
            "list": news_list,
            "total": total,
            "has_more": has_more
        }
    }

@router.get("/detail")
async def get_news_detail(news_id: int = Query(..., alias="id"), db: AsyncSession = Depends(get_db)):
    """
    获取新闻详情
    """
    # 先获取数据库中的新闻数据 -> 定义模型类 -> 封装获取数据方法
    news_detail = await crud_get_news_detail(db, news_id=news_id)
    if not news_detail:
        raise HTTPException(status_code=404, detail="新闻不存在")
    
    # 增加新闻浏览量
    views_result = await crud_increase_news_views(db, news_id=news_id)
    if not views_result:
        raise HTTPException(status_code=500, detail="增加新闻浏览量失败")
    
    # 获取相关新闻列表
    related_news = await crud_get_related_news(db, news_id=news_id, category_id=news_detail.category_id)

    return {
        "code": 200,
        "message": "获取新闻详情成功",
        "data": {
            "id": news_detail.id,
            "title": news_detail.title,
            "content": news_detail.content,
            "image": news_detail.image,
            "author": news_detail.author,
            "pushTime": news_detail.publish_time,
            "categoryId": news_detail.category_id,
            "views": news_detail.views,
            "relatedNews": related_news
        }
    }