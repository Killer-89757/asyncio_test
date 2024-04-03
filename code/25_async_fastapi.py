import asyncio

import aioredis
import uvicorn
from fastapi import FastAPI
from aioredis import Redis

app = FastAPI()
REDIS_POOL = aioredis.ConnectionPool("redis://127.0.0.1:8000",password="123456",minsize=1,maxsize=10)

@app.get("/")
def index():
    """普通操作接口"""
    return {"message":"hello world"}

@app.get("/red")
async def red():
    """异步操作接口"""
    print("请求来了")

    await asyncio.sleep(3)
    # 连接池获取一个链接
    conn = await REDIS_POOL.acquire()
    redis = Redis(conn)

    # 设置值
    await redis.hmset_dict("car",key1=1,key2=2)

    # 读取值
    result = await redis.hgetall("car",encoding="utf-8")
    print(result)

    # 连接归还连接池
    REDIS_POOL.release(conn)

    return result

if __name__ == "__main__":
    uvicorn.run("25_async_fastapi:app",host="127.0.0.1",port=5000,log_level="info")