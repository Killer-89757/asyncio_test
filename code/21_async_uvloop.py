import asyncio
import uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

# 编写asyncio的代码，与之前写的代码一致

# 内部的事件循环会自动变化为uvloop

asyncio.run(...)