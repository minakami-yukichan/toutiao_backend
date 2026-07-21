from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from schemas.users import UserRequest
from crud import users
from starlette import status

from utils.response import success_response
from schemas.users import UserAuthResponse, UserInfoResponse

router = APIRouter(prefix="/api/user", tags=["users"])

@router.post("/register")
async def register_user(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    # 注册逻辑: 验证用户是否存在 -> 创建用户 -> 生成token -> 返回用户信息和token
    existing_user = await users.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名已存在")
    
    # 创建用户
    user = await users.create_user(db, user_data)

    # 生成token
    token = await users.create_token(db, user.id)

    # return {
    #     "code": 200,
    #     "message": "注册成功",
    #     "data": {
    #         "token": token,
    #         "userInfo": {
    #             "id": user.id,
    #             "username": user.username,
    #             "bio": user.bio,
    #             "avatar": user.avatar,
    #         }
    #     }
    # }
    response_data = UserAuthResponse(token=token, user_info=UserInfoResponse.model_validate(user))
    return success_response(message="注册成功", data=response_data)

@router.post("/login")
async def login_user(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    # 登录逻辑: 验证用户是否存在 -> 验证用户名和密码 -> 生成token -> 返回用户信息和token
    user = await users.authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    token = await users.create_token(db, user.id)
    response_data = UserAuthResponse(token=token, user_info=UserInfoResponse.model_validate(user))

    return success_response(message="登录成功", data=response_data)

