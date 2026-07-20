from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class UserRequest(BaseModel):
    username: str
    password: str

# 基础类 + info 类
class UserInfoBase(BaseModel):
    """
    用户信息基础数据模型
    """
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="头像URL")
    gender: Optional[str] = Field(None, max_length=10, description="性别")
    bio: Optional[str] = Field(None, max_length=500, description="个人简介")

class UserInfoResponse(UserInfoBase):
    id: int
    username: str

    # 模型类配置
    model_config = ConfigDict(
        from_attributes=True  # 允许从 ORM 对象属性中取值
    )

# data 数据类型
class UserAuthResponse(BaseModel):
    token: str
    user_info: UserInfoResponse = Field(..., alias="userInfo")  # 使用别名 userInfo 来映射 user_info 字段

    # 添加模型类配置
    model_config = ConfigDict(
        populate_by_name=True,  # 允许通过字段名或别名进行数据填充
        from_attributes=True  # 允许从对象属性中填充数据
    )