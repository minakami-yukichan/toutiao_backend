from sqlalchemy import select
from sqlalchemy.orm import AsyncSession

from models.users import User
from schemas import security
from schemas.users import UserRequest
from utils.security import get_hashed_password

# 根据用户名查询数据库
async def get_user_by_username(db: AsyncSession, username: str):
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    return result.scalar_one_or_none()

# chuangjianyonghu
async def create_user(db: AsyncSession, user_data: UserRequest):
    # 先密码加密 -> add
    hashed_password = security.get_hashed_password(user_data.password)
    user = User(username=user_data.username, password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user) # 从数据库读取数据库最新的user
    return user