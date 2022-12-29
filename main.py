# 获取wallhaven的图片
import os
import requests
from lxml import etree
import time


def print_tags():  # 输出标签
    wallhaven_url = 'https://wallhaven.cc/'
    tags_xpath = '//a[@class="tagname sfw"]/text()'
    resp = requests.get(wallhaven_url)
    element = etree.HTML(resp.text)
    list1 = element.xpath(tags_xpath)
    for tag_content in list1:
        tag_content = '#' + tag_content
        print(f"\033[0;36;40m{tag_content}\033[0m", end='  ')  # 改变字体的前景色和背景色


def image_link_process(image_link: str) -> str:
    # https://w.wallhaven.cc/full/rd/wallhaven-rddgwm.jpg
    # https://th.wallhaven.cc/small/rd/rddgwm.jpg
    if "small" in image_link:
        image_link = image_link.replace("th", "w")
        image_link = image_link.replace("small", "full")
        url_path = image_link.split("/")
        url_path[-1] = f"wallhaven-{url_path[-1]}"
        return "/".join(url_path)
    return ""


print_tags()  # 输出标签
while 1:
    tag = input("\n请输入想搜索的内容标签：")
    url = f'https://wallhaven.cc/search?q={tag}'
    small_xpath = '//img[@alt="loading"]/@data-src'  # 小图片的xpath路径
    i = 0
    j = 0
    r = requests.get(url)
    e = etree.HTML(r.text)
    small_list = e.xpath(small_xpath)  # 获取一页小图片的链接
    pic_path = f'./Pictures/{tag}/'  # 根据用户输入的标签进行创建文件夹
    if not os.path.exists(pic_path):  # 检查是否存在
        os.mkdir(pic_path)
    for link in small_list:
        full_pic = image_link_process(link)  # 全屏壁纸
        fullpic_resp = requests.get(full_pic)
        if not fullpic_resp.status_code == 200:
            i = i + 1
            print(f"找不到图片！({i})")
        else:
            j = j + 1
            print(f'下载成功({j})')
            with open(f'./Pictures/{tag}/%s.jpg' % time.time(), 'wb') as f:  # 使用时间戳命名
                f.write(fullpic_resp.content)
    print(f"一共下载了{j}张图片，下载失败的图片一共有{i}张")
    answer = input("是否退出:")
    if answer == '是':
        break


# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。


def print_hi(name):
    # 在下面的代码行中使用断点来调试脚本。
    print(f'Hi, {name}')  # 按 Ctrl+F8 切换断点。


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    print_hi('PyCharm')

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
