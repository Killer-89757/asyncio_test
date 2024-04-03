import asyncio


async def func():
    print("周处除三害！！！")


result = func()  # 得到func协程对象

asyncio.run(result)
