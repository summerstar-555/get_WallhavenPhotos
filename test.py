# from multiprocessing import Process
# 
# num = 0
# 
# 
# def add():
#     global num
#     num = num + 1
# 
# 
# if __name__ == '__main__':
#     processes = [Process(target=add()) for i in range(5)]
#     for process in processes:
#         process.start()
#     for process in processes:
#         process.join()
#     print(num)
from multiprocessing import Process

# import requests
# from lxml import etree
#
# success_count = 0
#
#
# def download_pictures(page_num_fuc: int, tag: str):  # 一页一页地下载，一页有24张图片
#     """
#         :param page_num_fuc: 要下载的页面页码
#         :param tag: 要搜索的内容标签
#         :return: 无返回值
#     """
#     url = f'https://wallhaven.cc/search?q={tag}&page={page_num_fuc}'
#     # https://wallhaven.cc/search?q=anime&page=3
#     small_xpath = '//img[@alt="loading"]/@data-src'  # 小图片的xpath路径
#     global success_count
#     fail_count = 0  # 下载失败的图片数量
#     header = rand_ua()  # 调用随机生成ua的函数
#     m = 0  # 循环条件
#     while 1:  # 尝试三次，如果还是没响应就退出循环
#         try:
#             r = requests.get(url, timeout=10, headers=header)
#             break  # 成功连接则退出循环
#         except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):  # 如果五秒内没有响应，那么输出连接超时
#             print('连接超时，无法返回网页的响应！')
#             m = m + 1
#             if m == 3:
#                 exit(0)  # 直接终止整个程序
#     e = etree.HTML(r.text)
#     r.close()
#     small_list = e.xpath(small_xpath)  # 获取一页小图片的链接并放在列表中
#     is_dir(tag)  # 判断目录是否存在
#     for link in small_list:
#         full_pic = image_link_process(link)  # 全屏壁纸的链接
#         try:
#             fullpic_resp = requests.get(full_pic, timeout=10)
#         except requests.exceptions.ConnectTimeout or requests.exceptions.ReadTimeout:
#             print('服务器没有响应')
#             continue  # 跳过这一张图片的下载
#         if not fullpic_resp.status_code == 200:
#             fail_count = fail_count + 1
#             print(f"找不到图片！({fail_count})")
#         else:
#             success_count = success_count + 1
#             print(f'下载成功({success_count})')
#             with open(f'./Pictures/{tag}/%s.jpg' % time.time(), 'wb') as f:  # 使用时间戳命名
#                 f.write(fullpic_resp.content)
#     print(f"一共下载了{success_count}张图片，下载失败的图片一共有{fail_count}张")
# tag = 'Cyberpunk: Edgerunners'
# list1 = ['\\', '/', ':', '*', '?', '\"', '<', '>', '\'']        # 违规字符
# for char in tag:
#     if char in list1:  # 如果tag标签内有违规字符，那么替换成空格。并且因为这是函数内部，所以并不会对外面的tag造成影响
#         tag = tag.replace(char, ' ')
# print(tag)


# from main import download_pictures, success_count
# download_pictures(1, 'new year')
# print('成功下载的图片：', success_count)

import multiprocessing
import os
import time


# method为多次调用的方法
'''
def method(param):
    print(os.getpid())


if __name__ == '__main__':
    start = time.time()
    pool = multiprocessing.Pool(processes=5)
    params = ['param1', 'param2', 'param3', 'param4', 'param5']
    for param in params:
        pool.apply_async(method, args=(param,))
    pool.close()
    pool.join()
    print('主进程结束，用时：%.3f' % (time.time() - start))
'''
