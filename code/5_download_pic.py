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