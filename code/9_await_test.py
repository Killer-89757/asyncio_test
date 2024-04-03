import asyncio


async def func():
    print("来玩啊")
    response = await asyncio.sleep(1)  # response承接await等待对象执行的结果
    print("结束",response)

asyncio.run(func())