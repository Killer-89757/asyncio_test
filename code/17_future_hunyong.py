import time
import asyncio
import concurrent.futures

def func1():
    # 某个时间操作
    time.sleep(2)
    return "waws"

async def main():
    loop = asyncio.get_running_loop()

    # 1.run in the default loop's exector(默认是ThreadPoolExector)
    # 第一步：内部会先调用 ThreadPoolExector 的submit方法去线程池中申请一个线程去执行func1函数，并返回一个concurrent.futures.Future对象
    # 第二步：调用asyncio.wrap_future 将 concurrent.futures.Future对象包装成 asyncio.Future对象
    # 因为concurrent.futures.Future 对象不支持await语法，所以需要包装 asyncio.Future 对象才能使用
    fut = loop.run_in_executor(None,func1)
    result = await fut
    print("default thread pool",result)

    # 2.run in a custom thread pool
    # with concurrent.futures.ThreadPoolExecutor() as pool:
    #     result = await loop.run_in_executor(pool,func1)
    #     print("custom thread pool",result)

    # 2.run in a custom process pool
    # with concurrent.futures.ProcessPoolExecutor() as pool:
    #     result = await loop.run_in_executor(pool,func1)
    #     print("custom process pool",result)

asyncio.run(main())