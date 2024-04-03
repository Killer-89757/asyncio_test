import aiomysql
import asyncio


async def execute():
    # 网络IO操作，创建mysql连接
    conn = await aiomysql.connect(host='127.0.0.1', port="3306", user="root", password="111111", db="mysql")

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