# Single-file-Lightweight-Multi-threaded-4Chan-Threaded-Resource-Downloader
A single python source file to implement a multi-threaded resource crawler.

![img](img/sc.png)

## Environment（环境）

**Python3**

**Requests Module（Requests模块）**

How to installation Requests?（如何安装Requests？）

`pip3 install requests`

## How does it work?（如何使用？）

In a terminal with python installed, type..（在安装了 Python 的终端中，键入..）

`python3 4chan-downloader-n.py`

At this point it will ask you for the URL, just type it in and enter.（在这一点上，它会要求您输入URL，只需输入并按回车即可）

## How this code is implemented?（这个代码是如何实现的？）

After entering the URL: (输入URL后：)

①The regular expression will identify the thread name and the thread resource and its name.（①正则表达式将识别线程名称和线程资源及其名称）

② Create a folder according to the thread name (will replace / with -).（②依照线程名称创建文件夹（将替换/为-））

③After entering the folder, a multi-threaded download action will be performed.（③进入文件夹后将执行多线程下载动作）
