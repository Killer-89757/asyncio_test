import asyncio


async def func():
    print("周处除三害！！！")


result = func()  # 得到func协程对象

loop = asyncio.get_event_loop()
loop.run_until_complete(result)  # 将协程对象放入到事件循环中
