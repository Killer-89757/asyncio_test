import requests
import asyncio


async def download_image(url):
    print("开始下载：", url)

    loop = asyncio.get_event_loop()
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
