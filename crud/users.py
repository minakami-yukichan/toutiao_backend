from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from datetime import datetime, timedelta

from models.users import User, UserToken
from utils import security
from schemas.users import UserRequest
from utils.security import get_hashed_password

# 根据用户名查询数据库
async def get_user_by_username(db: AsyncSession, username: str):
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    return result.scalar_one_or_none()

# 创建用户
async def create_user(db: AsyncSession, user_data: UserRequest):
    # 先密码加密 -> add
    hashed_password = security.get_hashed_password(user_data.password)
    user = User(username=user_data.username, password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user) # 从数据库读取数据库最新的user
    return user

# 生成token
async def create_token(db: AsyncSession, user_id: int):
    # 生成token逻辑
    # 生成token -> 设置过期时间 -> 查询数据库当前用户是否有token -> 如果有则更新token和过期时间 -> 如果没有则创建新的token记录
    token = str(uuid.uuid4())
    expires_at = datetime.now() + timedelta(days=7)
    query = select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()
    if user_token:
        user_token.token = token
        user_token.expires_at = expires_at
    else:
        user_token = UserToken(user_id=user_id, token=token, expires_at=expires_at)
        db.add(user_token)
        await db.commit()
    
    return token

# 验证用户名和密码
async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_username(db, username)
    if not user:
        return None
    if not security.verify_password(password, user.password):
        return None
    return user