import re,threading,os
import requests as req

###################################################################
###################################################################
# Blog:hearyvens.com    Github:@Netpos-Dinmi(NegLongse | Hearyvens)
#                 Twitter : Hearyvens
# Youtube/Bilibili :   Hearyvens | NegLongse
# By:20230323 11:58 -- Hearyvens | NegLongse
###################################################################
###################################################################

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
        print("Download.."+files_name)
def multi_thread_down(files_names, files_urls):
    threads = []
    for  files_url,files_name in zip(files_urls, files_names):
        threads.append(threading.Thread(target=down, args=(files_name, files_url)))
    for thread in threads:
        thread.start()

r = req.get(url,headers=headers)
if __name__ == '__main__':
    s = re.findall(r'<a href="\/\/(i.4cdn.org.*?)".*?>(.*?)<\/a>', r.text)
    if len(s) == 0:
        r = req.get(url,headers=headers)
        s = re.findall(r'<a href="\/\/(is2.4chan.org.*?)".*?>(.*?)<\/a>', r.text)

    p = re.findall(r'<input type="checkbox" .* value="delete"> <span class="subject">(.*?)<\/span> <span class="nameBlock"><span class="name">(.*?)<\/span>', r.text)

    folder_path_name = p[0][0]
    new_folder_path_name = str(folder_path_name).replace("/","-")
    if len(p[0][0]) == 0:
        p = re.findall(r'<span class="name">.*?<\/span>.*?class="dateTime".*?<blockquote class="postMessage".*?>(.*?)<\/blockquote>', r.text)
        folder_path_name = p[0]
        new_folder_path_name = str(folder_path_name).replace("/","-") and str(folder_path_name).replace("<br>","") 
    print("mkdir" + new_folder_path_name)
        
    os.mkdir(new_folder_path_name)
    os.chdir(new_folder_path_name)
        
    for item in s:
        files_name = item[1]
        files_url = "https://" + item[0]
        files_names.append(files_name)
        files_urls.append(files_url)

    multi_thread_down(files_names, files_urls)

