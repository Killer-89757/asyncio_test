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
    # asyncio.run(main())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())