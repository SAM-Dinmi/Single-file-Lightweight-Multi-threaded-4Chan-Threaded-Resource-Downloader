import re
import threading
import os
import requests as req
from concurrent.futures import ThreadPoolExecutor

###################################################################
###################################################################
# Blog:hearyvens.com    Github:@Netpos-Dinmi(NegLongse | Hearyvens)
#                 Twitter : Hearyvens
# Youtube/Bilibili :   Hearyvens | NegLongse
# By:20230323 11:58 -- Hearyvens | NegLongse
###################################################################
###################################################################

# 设置 HTTP 请求头
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
}

# 全局变量存储文件名和文件 URL
files_names = []
files_urls = []

# 创建一个全局的 requests.Session 来复用连接
session = req.Session()

# 清理文件名中的非法字符
def sanitize_filename(filename):
    return re.sub(r'[\\/:"*?<>|]', '_', filename)

# 文件下载函数
def down(files_name, files_url):
    try:
        # 清理文件名中的非法字符
        files_name = sanitize_filename(files_name)
        
        # 开始下载文件
        with session.get(files_url, headers=headers, stream=True, timeout=10) as response:
            response.raise_for_status()  # 检查 HTTP 请求是否成功
            with open(files_name, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
        print(f"Download complete: {files_name}")
    except Exception as e:
        print(f"Error downloading {files_name}: {e}")

# 多线程下载函数
def multi_thread_down(files_names, files_urls):
    max_threads = 10  # 设置最大线程数量
    with ThreadPoolExecutor(max_threads) as executor:
        for files_url, files_name in zip(files_urls, files_names):
            executor.submit(down, files_name, files_url)

# 分批次下载函数（避免过多任务导致资源耗尽）
def batch_download(files_names, files_urls, batch_size=50):
    total_files = len(files_names)
    for i in range(0, total_files, batch_size):
        batch_names = files_names[i:i + batch_size]
        batch_urls = files_urls[i:i + batch_size]
        multi_thread_down(batch_names, batch_urls)

# 主程序入口
if __name__ == '__main__':
    # 输入目标 URL
    url = input("Please enter URL: ")
    
    # 请求目标页面
    r = req.get(url, headers=headers)
    if r.status_code != 200:
        print(f"Failed to fetch the page. Status code: {r.status_code}")
        exit()

    # 使用正则表达式提取文件链接和名称
    s = re.findall(r'<a href="\/\/(i.4cdn.org.*?)".*?>(.*?)<\/a>', r.text)
    if len(s) == 0:
        # 如果第一个正则失败，尝试第二个正则
        s = re.findall(r'<a href="\/\/(is2.4chan.org.*?)".*?>(.*?)<\/a>', r.text)

    # 如果仍然没有匹配到文件，退出程序
    if len(s) == 0:
        print("No files found on the page.")
        exit()

    # 遍历匹配结果，存储文件名和 URL
    for item in s:
        files_name = item[1].strip() or "unnamed_file"  # 如果文件名为空，设置为默认值
        files_url = "https://" + item[0].strip()  # 拼接完整 URL
        files_names.append(files_name)
        files_urls.append(files_url)

    # 提取页面的标题作为文件夹名
    folder_name = re.search(r'<title>(.*?)<\/title>', r.text)
    folder_name = folder_name.group(1) if folder_name else "downloads"
    folder_name = sanitize_filename(folder_name)  # 清理非法字符

    # 创建下载文件夹
    try:
        os.makedirs(folder_name, exist_ok=True)
        os.chdir(folder_name)
    except Exception as e:
        print(f"Error creating directory {folder_name}: {e}")
        exit()

    # 开始分批次下载文件
    print(f"Starting download... Total files: {len(files_names)}")
    batch_download(files_names, files_urls, batch_size=50)
    print("All downloads completed.")
