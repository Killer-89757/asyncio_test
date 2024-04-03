# 协程 & asyncio & 异步

主讲：武佩奇

网络地址：https://www.bilibili.com/video/BV17A4m1P7L3/?spm_id_from=333.337.search-card.all.click&vd_source=e7f81b05fc7b50403bf3a758724be4c9

时间：2024年4月4日

##  part-1

### 基础

1. **为什么要讲？**
   - 异步非阻塞、asyncio很重要
   - tornado、fastapi、django 3.x asgi、aiohttp、常见的应用使用异步非阻塞的形式、提升性能

2. **如何进行讲解？**
   - 协程的概念
   - asyncio异步编程模块
   - 实战案例

### 协程

协程不是计算机提供的，程序员人为创造出来的。

协程（Coroutine）,也可以被称为微线程，是一种用户态内的上下文切换技术。简而言之，其实就是通过一个线程实现代码块相互切换执行，例如：

```python
def func1():
	print(1)
	...
	print(2)
	
def func2():
	print(3)
	...
	print(4)

func1()
func2()
```

实现协程有这么几种方法：

- greenlet，很早期的模块
- yield关键字
- asyncio装饰器(py3.4)
- async、await关键字(py3.5) [官方推荐]

#### greenlet 实现协程

> pip install greenlet

```python
from greenlet import greenlet


def func1():
    print(1)      # 第二步 输出1
    gr2.switch()  # 第三步 切换func2函数
    print(1)      # 第六步 输出2
    gr2.switch()  # 第七步 切换func2函数


def func2():
    print(3)       # 第四步 输出3
    gr1.switch()   # 第五步 切换func1函数
    print(4)       # 第八步 输出4
    gr1.switch()   # 第九步 切换func1函数


gr1 = greenlet(func1)
gr2 = greenlet(func2)
gr1.switch()     # 第一步 去执行func1函数
```

执行结果

![](https://cdn.jsdelivr.net/gh/Killer-89757/PicBed/images/2024%2F04%2Fimage-20240403213022656-81ec6d.png)

#### yield关键字

其实使用yield构建的是生成器函数，使用for循环就是相当于单步的next进行代码运行

```python
def func1():
    yield 1
    yield from func2()
    yield 2


def func2():
    yield 3
    yield 4


f1 = func1()
for item in f1:
    print(item)
```

![](https://cdn.jsdelivr.net/gh/Killer-89757/PicBed/images/2024%2F04%2Fimage-20240403213621198-a21e18.png)

#### asyncio装饰器

在python 3.4以及之后的版本

```python
import asyncio

@asyncio.coroutine
def func1():
    print(1)
    yield from asyncio.sleep(2) #遇到IO耗时操作，自动化切换到tasks中的其他任务
    print(2)

@asyncio.coroutine
def func2():
    print(3)
    yield from asyncio.sleep(2) #遇到IO耗时操作，自动化切换到tasks中的其他任务
    print(4)

tasks = [
    asyncio.ensure_future(func1()),
    asyncio.ensure_future(func2())
]

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))
```

注意：警告部分其实使装饰器的写法在python3.4之后被async关键字的方式替代了，所以警告

coroutine 协程，普通函数加上`asyncio.coroutine`变成协程函数，不能通过简单的调用执行，需要将其变成**任务**，放在**事件循环**中完成

将两个协程函数放到一个线程中去，随机执行对应的代码，当遇到IO耗时操作(等待)，**自动切换**到其他可执行的协程函数中去执行

> 注意：
>
> - 上面我们使用greenlet、yield的方式都是手动设置完成切换
> - 使用asyncio的方式，遇到IO阻塞自动切换

![](https://cdn.jsdelivr.net/gh/Killer-89757/PicBed/images/2024%2F04%2Fimage-20240403214923419-d385a8.png)

#### async & await关键字

在python 3.5以及之后的版本

```python
import asyncio


async def func1():
    print(1)
    await asyncio.sleep(2) #遇到IO耗时操作，自动化切换到tasks中的其他任务
    print(2)

async def func2():
    print(3)
    await asyncio.sleep(2) #遇到IO耗时操作，自动化切换到tasks中的其他任务
    print(4)

tasks = [
    asyncio.ensure_future(func1()),
    asyncio.ensure_future(func2())
]

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))
```

![](https://cdn.jsdelivr.net/gh/Killer-89757/PicBed/images/2024%2F04%2Fimage-20240403220544699-392536.png)

### 协程意义

> 意义：在一个线程中如果遇到IO等待的时间，线程不会傻傻等，利用空闲时间再去干点其他事

案例：下载三张图片(网络IO)

- 普通方式(同步)

```python
import requests

def download_image(url):
    print("开始下载：",url)
    # 发送网络请求，下载图片
    response = requests.get(url)
    print("下载完成")
    file_name = url.rsplit("-")[-1]
    with open(file_name,mode="wb") as file_object:
        file_object.write(response.content)

if __name__ == "__main__":
    url_list = [
        "https://cdn.jsdelivr.net/gh/Killer-89757/PicBed/images/2024%2F03%2F20240322202303-48a7ac.png",
        "https://cdn.jsdelivr.net/gh/Killer-89757/PicBed/images/2024%2F03%2F_r-ad3532.jpg",
        "https://cdn.jsdelivr.net/gh/Killer-89757/PicBed/images/2024%2F03%2F332jv-4b7203.jpg"
    ]
    for item in url_list:
        download_image(item)
```

- asyncio方式(异步)

```python
import aiohttp
import asyncio

async def fetch(session,url):
    print("发送请求：",url)
    async with session.get(url,verify_ssl=False) as response:
        content = await response.content.read()
        print("下载完成")
        file_name = url.rsplit("-")[-1]
        with open(file_name,mode="wb") as file_object:
            file_object.write(content)

async def main():
    async with aiohttp.ClientSession() as session:
        url_list = [
            "https://cdn.jsdelivr.net/gh/Killer-89757/PicBed/images/2024%2F03%2F20240322202303-48a7ac.png",
            "https://cdn.jsdelivr.net/gh/Killer-89757/PicBed/images/2024%2F03%2F_r-ad3532.jpg",
            "https://cdn.jsdelivr.net/gh/Killer-89757/PicBed/images/2024%2F03%2F332jv-4b7203.jpg"
        ]
        tasks = [asyncio.create_task(fetch(session,url)) for url in url_list]
        await asyncio.wait(tasks)

if __name__ == "__main__":
    asyncio.run(main())
```

## part-2

### 异步编程

#### 事件循环

理解成为一个死循环，去检测和执行某些代码

```python
# 伪代码
任务列表 = [任务1，任务2，任务3....]

while True:
    可执行的任务列表，已经完成的任务列表 = 去任务列表中检查所有任务，将"可执行" 和 "已完成" 的任务返回
    
    for 就绪任务 in 已经准备就绪的任务列表:
        执行已就绪的任务
        
    for 已经完成的任务 in 已经完成的任务列表:
        在任务列表中移除 已完成的任务
        
  	如果 任务列表 中的任务都已经完成，则终止循环
```

```python
import asyncio

# 去生成或获取一个时间循环
loop = asyncio.get_event_loop()

# 将任务放到"任务列表"
loop.run_until_complete(任务)
```

#### 快速上手

协程函数，定义函数的时候 `async def 函数名`

协程对象， 执行 协程函数() 得到的就是协程对象

```python
async def func():
    pass

result = func() # 得到func协程对象
```

注意：执行协程函数创建协程对象，函数内部代码并不会执行。

执行协程函数内部代码：必须要将协程对象交给事件循环进行处理

- 之前的写法

```python
import asyncio

async def func():
    print("周处除三害！！！")

result = func() # 得到func协程对象

loop = asyncio.get_event_loop()
loop.run_until_complete( result ) #将协程对象放入到事件循环中
```

- python 3.7 之后的写法

```python
import asyncio

async def func():
    print("周处除三害！！！")

result = func() # 得到func协程对象

asyncio.run( result )
```

#### await

await + **可等待的对象**(协程对象、Future、Task对象 -> IO等待)

```python
import asyncio

async def func():
    print("来玩啊")
    response = await asyncio.sleep(1)  # response承接await等待对象执行的结果
    print("结束",response)

asyncio.run(func())
```

- 执行流程：
  - **先将协程对象放入到事件循环中，然后执行协程代码，输出"来玩啊"，接下来进入IO等待，此时线程从当前协程中切换到其他协程，执行对应代码，当IO等待结束，线程调度回到当前线程，将IO结果放入到response，输出"结束，None"，当前协程执行完成，线程也执行结束，程序结束**

![](https://cdn.jsdelivr.net/gh/Killer-89757/PicBed/images/2024%2F04%2Fimage-20240403230733767-cd0c36.png)

示例1：

```python
import asyncio

async def others():
    print("start")
    await asyncio.sleep(2)
    print("end")
    return "返回值"

async def func():
    print("执行协程函数内部代码")
    # 当遇到IO操作挂起当前协程(任务),等IO操作完成之后再继续往下执行
    # 当前协程挂起时，事件循环可以去执行其他协程(任务)
    response = await others()
    print("IO的请求结束，结果是：",response)

asyncio.run(func())
```

![](https://cdn.jsdelivr.net/gh/Killer-89757/PicBed/images/2024%2F04%2Fimage-20240403231554975-7b33b7.png)

示例2：

```python
import asyncio

async def others():
    print("start")
    await asyncio.sleep(2)
    print("end")
    return "返回值"

async def func():
    print("执行协程函数内部代码")
    # 当遇到IO操作挂起当前协程(任务),等IO操作完成之后再继续往下执行
    # 当前协程挂起时，事件循环可以去执行其他协程(任务)
    response1 = await others()
    print("IO的请求结束，结果是：",response1)
    
    response2 = await others()
    print("IO的请求结束，结果是：",response2)

asyncio.run(func())
```

await就是等待对象的值得到结果之后再向下走。

#### Task对象

> 在事件循环中添加多个任务
>
> Tasks 用于并发调度协程，通过`asyncio.create_task(协程对象)`的方式创建Task对象，这样可以让协程加入事件循环中等待被调度执行。除了使用
>
> `asyncio.create_task(协程对象)`函数以外，还可以使用低层次的`loop.create_task()`或者`ensure_future()`函数。不建议手动实例化Task对象

注意：`asyncio.create_task(协程对象)`函数在python 3.7 中加入的。在python 3.7之前 ，可以改用低层级的`asyncio.ensure_future()`函数

- 普通代码

```python
import asyncio

async def func():
    print("1")
    await asyncio.sleep(2)
    print(2)
    return "返回值"

async def main():
    print("开始")
	
    # 创建task对象，将当前执行func函数任务添加到事件循环
    task1 = asyncio.create_task(func())
    task2 = asyncio.create_task(func())

    print("main结束")

    # 当执行某协程遇到IO操作时候，会自动切换执行其他任务
    # 此处的await是等待相对应的协程全都执行完毕并获取结果
    ret1 = await task1
    ret2 = await task2
    print(ret1,ret2)

asyncio.run(main())
```

![](https://cdn.jsdelivr.net/gh/Killer-89757/PicBed/images/2024%2F04%2Fimage-20240403234400649-a1d5b8.png)

- 常用代码

```python
import asyncio


async def func():
    print("1")
    await asyncio.sleep(2)
    print(2)
    return "返回值"


async def main():
    print("开始")

    # 创建task对象，将当前执行func函数任务添加到事件循环
    task_list = [
        asyncio.create_task(func())
        asyncio.create_task(func())
    ]

    print("main结束")

    # 当执行某协程遇到IO操作时候，会自动切换执行其他任务
    # 此处的await是等待相对应的协程全都执行完毕并获取结果
    done, pending = await asyncio.wait(task_list,timeout=None)
    print(done)


asyncio.run(main())
```

![](https://cdn.jsdelivr.net/gh/Killer-89757/PicBed/images/2024%2F04%2Fimage-20240403235230690-bad7a2.png)

当设置timeout的值为1的时候，看下`pending`的值

![](https://cdn.jsdelivr.net/gh/Killer-89757/PicBed/images/2024%2F04%2Fimage-20240403235507277-cc6a73.png)

我们可以在create_task的时候，给不同的task进行命名。

```python
import asyncio


async def func():
    print("1")
    await asyncio.sleep(2)
    print(2)
    return "返回值"


async def main():
    print("开始")

    # 创建task对象，将当前执行func函数任务添加到事件循环
    task_list = [
        asyncio.create_task(func(),name="n1")
        asyncio.create_task(func(),name="n2")
    ]

    print("main结束")

    # 当执行某协程遇到IO操作时候，会自动切换执行其他任务
    # 此处的await是等待相对应的协程全都执行完毕并获取结果
    done, pending = await asyncio.wait(task_list,timeout=None)
    print(done)


asyncio.run(main())
```

![](https://cdn.jsdelivr.net/gh/Killer-89757/PicBed/images/2024%2F04%2Fimage-20240403235811701-7cfc3a.png)

- 示例

```python
# 错误代码
import asyncio

async def func():
    print("1")
    await asyncio.sleep(2)
    print(2)
    return "返回值"

# 这个部分代码存在错误，run的时候才会创建事件循环，但是我们还没创建事件循环之前，就将协程对象加入到事件循环中，所以出现错误    
task_list = [
    asyncio.create_task(func(),name="n1")
    asyncio.create_task(func(),name="n2")
]

done,pending = asyncio.run(asyncio.wait(task_list))
print(done)
```

```python
# 正确代码
import asyncio

async def func():
    print("1")
    await asyncio.sleep(2)
    print(2)
    return "返回值"

# 在这个地方只加入协程对象，构建协程对象列表   
task_list = [
    func(),
    func()
]

# 在wait方法中会自动将其创建成任务并加入到事件循环中
done,pending = asyncio.run(asyncio.wait(task_list))
print(done)
```

#### asyncio.Future对象

是Task的基类

> A Future is a special low-level awaitable object that represents an eventual result of an asynchronous operation
>
> Future 是一种特殊的低级可等待对象，代表异步操作的最终结果

Task继承Future，task对象内部await结果的处理基于Future对象来的

- 普通代码

```python
import asyncio
async def main():
    # 获取当前的事件循环
    loop = asyncio.get_running_loop()
    
    # 创建一个任务(future对象)，这个任务什么都不干
    fut = loop.create_future()
    
    # 等待任务最终结果(future对象)，没有结果则会一直等下去
    await fut

asyncio.run(main())

# 运行结果：程序一直卡住不动
```

- 进阶用法

```python
import asyncio
async def set_after(fut):
    await asyncio.sleep(2)
    fut.set_result("222")

async def main():
    # 获取当前的事件循环
    loop = asyncio.get_running_loop()

    # 创建一个任务(future对象)，没绑定任何行为，则这个任务永远不知道什么时候结束
    fut = loop.create_future()

    # 创建一个任务(Task对象)，绑定了set_after函数，函数内部在2s之后，会给fut赋值
    # 即手动设置future任务的最终结果，那么fut就可以结束了
    await loop.create_task(set_after(fut))
    data = await fut
    print(data)

asyncio.run(main())
```

#### concurrent.future.Future对象

使用线程池、进程池实现异步操作时用到的对象

```python
import time
from concurrent.futures import Future
from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures.process import ProcessPoolExecutor


def func(value):
    time.sleep(1)
    print(value)


# 创建线程池
pool = ThreadPoolExecutor(max_workers=5)

# 创建进程池
# pool = ProcessPoolExecutor(max_workers=5)

for i in range(10):
    fut = pool.submit(func, i)
    print(fut)
```

![](https://cdn.jsdelivr.net/gh/Killer-89757/PicBed/images/2024%2F04%2Fimage-20240404003139800-00d23d.png)

这个future对象也是用来等待线程、进行对象的运行结果的

以后写代码`协程future对象`和`线程\进程 future 对象`可能会混用

例如：crm项目 80% 都是基于协程异步编程 + XXXX模块(模块比较老、不支持协程，基于线程、进程来做异步编程)

- 混用代码

```python
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
```

案例：asyncio + 不支持异步的模块

```python
import requests
import asyncio


async def download_image(url):
    print("开始下载：", url)

    loop = asyncio.get_event_loop()
    # requests模块默认不支持异步操作，所以使用线程池来配合实现了
    future = loop.run_in_executor(None, requests.get, url)
    response = await future
    print("下载完成")
    file_name = url.rsplit("-")[-1]
    with open(file_name, mode="wb") as file_object:
        file_object.write(response.content)


if __name__ == "__main__":
    url_list = [
        "https://cdn.jsdelivr.net/gh/Killer-89757/PicBed/images/2024%2F03%2F20240322202303-48a7ac.png",
        "https://cdn.jsdelivr.net/gh/Killer-89757/PicBed/images/2024%2F03%2F_r-ad3532.jpg",
        "https://cdn.jsdelivr.net/gh/Killer-89757/PicBed/images/2024%2F03%2F332jv-4b7203.jpg"
    ]
    tasks = [download_image(url) for url in url_list]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))

```

#### 异步迭代器

**什么是异步迭代器？**

实现了`__aiter__()` 和 `__anext__()` 方法的对象。`__anext__ `必须返回一个`awaitable`对象。`async for`会处理异步迭代器的 `__anext__()` 方法所返回的可等待对象。直到其引发一个`StopAsyncIteration`异常。

**什么是异步可迭代对象？**

可以在 `async for` 语句中被使用的对象。必须通过他的 `__aiter__()` 方法返回一个`asynchronous iterator`

```python
import asyncio

class Reader(object):
    def __init__(self):
        self.count = 0

    async def readline(self):
        self.count += 1
        if self.count == 100:
            return None
        return self.count

    def __aiter__(self):
        return self

    async def __anext__(self):
        val = await self.readline()
        if val == None:
            raise StopAsyncIteration
        return val

async def func():
    obj = Reader()
    async for item in obj:
        print(item)

asyncio.run(func())
```

`async for` 必须写在一个协程函数中

![](https://cdn.jsdelivr.net/gh/Killer-89757/PicBed/images/2024%2F04%2Fimage-20240404011807775-ea6859.png)

#### 异步上下文管理

对象通过定义`__aenter__()` 和 `__aexit__()`方法来对 `async with`语句中的环境进行控制

```python
import asyncio


class AsyncContextManager:
    def __init__(self):
        self.conn = conn

    async def do_something(self):
        # 异步连接数据库
        return "666"

    async def __aenter__(self):
        self.conn = await asyncio.sleep(1)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await asyncio.sleep(1)


async def func():
    async with AsyncContextManager() as f:
        result = await f.do_something()
        print(result)

asyncio.run(func())
```

`async with` 必须写在一个协程函数中

### uvloop

是asyncio的事件循环的替代方案，**uvloop事件循环 `效率` 是 默认asyncio的事件循环 至少 2 倍以上**

 ```python
import asyncio
import uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

# 编写asyncio的代码，与之前写的代码一致

# 内部的事件循环会自动变化为uvloop
asyncio.run(...)
 ```

![](https://cdn.jsdelivr.net/gh/Killer-89757/PicBed/images/2024%2F04%2Fimage-20240404014346915-a2a5bf.png)

注意事项： 

一个 asgi  ->  uvicorn -> 快的核心原因是 uvloop 

## part-3

### 异步redis

在使用python代码操作redis时，连接、操作、断开都是网络IO

```
pip install aioredis
```

示例：

```python
import aioredis
import asyncio

async def execute(address,password):
    print("开始执行",address)
    # 网络IO操作，创建redis连接
    
    redis = await aioredis.create_redis(address,password=password)
    # 网络IO操作，在redis中设置hash值，内部在设三个键值对
    # redis ={ "car":{key1:1,key2:2,key3:3}}
    await redis.hmset_dict("car",key1=1,key2=2,key3=3)
    
    # 网络IO操作，从redis中获取值
    result = await redis.hgetall("car",encoding="utf-8")
    print(result)
    
    redis.close()
    # 网络IO操作:关闭redis连接
    await redis.wait_closed()
    
    print("结束",address)

asyncio.run(execute("redis://127.0.0.1","root1234"))
```

示例2：

```python
import aioredis
import asyncio

async def execute(address,password):
    print("开始执行",address)
    # 网络IO操作，创建redis连接
    
    redis = await aioredis.create_redis(address,password=password)
    # 网络IO操作，在redis中设置hash值，内部在设三个键值对
    # redis ={ "car":{key1:1,key2:2,key3:3}}
    await redis.hmset_dict("car",key1=1,key2=2,key3=3)
    
    # 网络IO操作，从redis中获取值
    result = await redis.hgetall("car",encoding="utf-8")
    print(result)
    
    redis.close()
    # 网络IO操作:关闭redis连接
    await redis.wait_closed()
    
    print("结束",address)

task_list = [
    execute("redis://127.0.0.1:8000","root1234"),
    execute("redis://127.0.0.1:9000","root5678")
]

asyncio.run(asyncio.wait(task_list))
```

### 异步MySQL

在使用python代码操作redis时，连接、操作、断开都是网络IO

```python
pip install aiomysql
```

示例：

```python
import aiomysql
import asyncio

async def execute():
    # 网络IO操作，创建mysql连接
    conn = await aiomysql.connect(host='127.0.0.1',port="3306",user="root",password="111111",db="mysql")
    
    # 网络IO操作，创建cursor
    cur = await conn.cursor()
    
    # 网络IO操作，执行sql
    await cur.execute("select host from user")

    # 网络IO操作，获取sql结果
    result = await cur.fetchall()
    print(result)

    
    # 网络IO操作:关闭mysql连接
    await cur.close()
   	conn.close()

asyncio.run(execute())
```

### FastAPI异步框架

```python
pip install fastapi
```

```python
pip install uvicorn (asgi内部基于uvloop)
```

示例：

```python
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
```

### 异步爬虫

```python
import aiohttp
import asyncio

async def fetch(session,url):
    print("发送请求：",url)
    async with session.get(url,verify_ssl=False) as response:
        text = await response.text()
        print("得到结果",url,len(text))

async def main():
    async with aiohttp.ClientSession() as session:
        url_list = [
            "https://python.org",
            "https://www.baidu.com",
            "https://www.weibo.com"
        ]
        tasks = [asyncio.create_task(fetch(session,url)) for url in url_list]
        await asyncio.wait(tasks)

if __name__ == "__main__":
    asyncio.run(main())
```

