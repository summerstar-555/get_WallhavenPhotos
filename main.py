# 获取wallhaven的图片
import os
import requests
from lxml import etree
import time
from search_result import search_result
import os
from multiprocessing import Process


def print_tags():  # 输出标签
    wallhaven_url = 'https://wallhaven.cc/'
    tags_xpath = '//a[@class="tagname sfw"]/text()'
    resp = requests.get(wallhaven_url, timeout=10)
    element = etree.HTML(resp.text)
    list1 = element.xpath(tags_xpath)
    for tag_content in list1:
        tag_content = '#' + tag_content
        print(f"\033[0;36;40m{tag_content}\033[0m", end='  ')  # 改变字体的前景色和背景色


def is_dir(tag: str):
    pic_path = f'./Pictures/{tag}/'  # 根据用户输入的标签进行创建文件夹
    if not os.path.exists('./Pictures'):
        os.mkdir('./Pictures')
    if not os.path.exists(pic_path):  # 检查是否存在
        os.mkdir(pic_path)


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


def download_pictures(page_num: int, tag: str):  # 一页一页地下载，一页有24张图片
    # while 1:      # 去掉循环，改用多线程
    # page_num = 1
    url = f'https://wallhaven.cc/search?q={tag}&page={page_num}'
    # https://wallhaven.cc/search?q=anime&page=3
    small_xpath = '//img[@alt="loading"]/@data-src'  # 小图片的xpath路径
    i = 0  # 成功下载的图片数量
    j = 0  # 下载失败的图片数量
    m = 0  # 循环条件
    while 1:  # 尝试三次，如果还是没响应就退出循环
        try:
            r = requests.get(url, timeout=10)
            break  # 成功连接则退出循环
        except requests.exceptions.ConnectTimeout or requests.exceptions.ReadTimeout:  # 如果五秒内没有响应，那么输出连接超时
            print('连接超时，无法返回网页的响应！')
            m = m + 1
            if m == 3:
                exit(0)  # 直接终止整个程序
    e = etree.HTML(r.text)
    small_list = e.xpath(small_xpath)  # 获取一页小图片的链接并放在列表中
    is_dir(tag)                   # 判断目录是否存在
    for link in small_list:
        full_pic = image_link_process(link)  # 全屏壁纸的链接
        try:
            fullpic_resp = requests.get(full_pic, timeout=10)
        except requests.exceptions.ConnectTimeout or requests.exceptions.ReadTimeout:
            print('服务器没有响应')
            continue        # 跳过这一张图片的下载
        if not fullpic_resp.status_code == 200:
            i = i + 1
            print(f"找不到图片！({i})")
        else:
            j = j + 1
            print(f'下载成功({j})')
            with open(f'./Pictures/{tag}/%s.jpg' % time.time(), 'wb') as f:  # 使用时间戳命名
                f.write(fullpic_resp.content)
    print(f"一共下载了{j}张图片，下载失败的图片一共有{i}张")
    page_num = page_num + 1
    os.system('cls')
    # print('开始下一页的下载')
    # answer = input("是否退出:")
    # if answer == '是':
    #     break


if __name__ == '__main__':
    # print_tags()  # 输出标签
    # tag1 = input("\n请输入想搜索的内容标签：")
    # tag2 = input("\n请输入想搜索的内容标签：")
    # # 从这里开始显示查找标签的结果
    # if not search_result(tag1):
    #     pass
    # else:
    #     p1 = Process(target=download_pictures, args=(1, tag1))
    #     p2 = Process(target=download_pictures, args=(1, tag2))
    #     p1.start()
    #     p2.start()
    #     p1.join()
    for i in range(1, 10):
        download_pictures(i, 'anime')
