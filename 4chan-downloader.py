import re,threading,os
import requests as req

url = input("Please enter URL:")

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
}

files_names =[]
files_urls = []

def down(files_name,files_url):
    with open(files_name, "wb")as file:
        i = req.get(files_url,headers=headers)
        file.write(i.content)

def multi_thread_down(files_names, files_urls):
    threads = []
    for  files_url,files_name in zip(files_urls, files_names):
        threads.append(threading.Thread(target=down, args=(files_name, files_url)))
    for thread in threads:
        thread.start()

r = req.get(url,headers=headers)
# s = re.findall(r'<a href="\/(\/.*?)".*?>(.*?)<\/a>', r.text)
# for item in s:
#     if item[0].endswith('/'):
#         print("shabi")
#     else:
#         print(item)

if __name__ == '__main__':

    s = re.findall(r'<a href="\/\/(i.4cdn.org.*?)".*?>(.*?)<\/a>', r.text)
    for item in s:
        files_name = item[1]
        files_url = "https://" + item[0]
        files_names.append(files_name)
        files_urls.append(files_url)

    multi_thread_down(files_names, files_urls)

