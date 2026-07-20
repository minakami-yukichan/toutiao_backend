from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import news, users
from utils.exception_handler import register_exception_handler

app = FastAPI()

# 注册异常处理器
register_exception_handler(app)  # 注册全局异常处理器

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，开发时允许所有，生产环境需要指定源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有请求头
)

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}

# 挂载路由
app.include_router(news.router)

app.include_router(users.router)