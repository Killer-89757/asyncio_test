import aioredis
import asyncio


async def execute(address, password):
    print("开始执行", address)
    # 网络IO操作，创建redis连接

    redis = await aioredis.create_redis(address, password=password)
    # 网络IO操作，在redis中设置hash值，内部在设三个键值对
    # redis ={ "car":{key1:1,key2:2,key3:3}}
    await redis.hmset_dict("car", key1=1, key2=2, key3=3)

    # 网络IO操作，从redis中获取值
    result = await redis.hgetall("car", encoding="utf-8")
    print(result)

    redis.close()
    # 网络IO操作:关闭redis连接
    await redis.wait_closed()

    print("结束", address)


task_list = [
    execute("redis://127.0.0.1:8000", "root1234"),
    execute("redis://127.0.0.1:9000", "root5678")
]

asyncio.run(asyncio.wait(task_list))