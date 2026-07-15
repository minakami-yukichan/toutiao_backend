from fastapi import FastAPI

from routers import news

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}

# 挂载路由
app.include_router(news.router)