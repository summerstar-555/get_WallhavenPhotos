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
#             full_pic_resp = requests.get(full_pic, timeout=10)
#         except requests.exceptions.ConnectTimeout or requests.exceptions.ReadTimeout:
#             print('服务器没有响应')
#             continue  # 跳过这一张图片的下载
#         if not full_pic_resp.status_code == 200:
#             fail_count = fail_count + 1
#             print(f"找不到图片！({fail_count})")
#         else:
#             success_count = success_count + 1
#             print(f'下载成功({success_count})')
#             with open(f'./Pictures/{tag}/%s.jpg' % time.time(), 'wb') as f:  # 使用时间戳命名
#                 f.write(full_pic_resp.content)
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
from urllib import response

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

# 每个进程的工作量 = 每一页24张图片 / 进程数
# 例如：
# 4进程，每个进程的工作量为： 24 / 4 = 6
# 8进程，每个进程的工作量为： 24 / 8 = 3
# 每个进程都需要进行
# 1.从小图片列表中拿出属于自己的跟自己工作量相关的图片链接
# 2.转换为大图片链接
# 3.连接服务器，可能报错，报错则抛出异常并跳过这一张图片。判断状态码
# 如果状态码是200，那么
#   写入
# 如果是404
#   将链接修改然后进行第3步，但只会执行一次
# 断开与服务器的连接，以免请求过多
# 进程与进程最大的区别就是下载任务的不同

# from multiprocessing import Pool
# import time
# processes_count = 4  # 进程数
# start_time = time.time()
# small_list = ['https://th.wallhaven.cc/small/z8/z851ev.jpg', 'https://th.wallhaven.cc/small/z8/z85pow.jpg', 'https://th.wallhaven.cc/small/dp/dpw27g.jpg', 'https://th.wallhaven.cc/small/x8/x8p95l.jpg', 'https://th.wallhaven.cc/small/kw/kwm527.jpg', 'https://th.wallhaven.cc/small/m9/m981jm.jpg', 'https://th.wallhaven.cc/small/95/957j71.jpg', 'https://th.wallhaven.cc/small/gp/gp7xme.jpg', 'https://th.wallhaven.cc/small/l3/l3ew52.jpg', 'https://th.wallhaven.cc/small/pk/pkyojp.jpg', 'https://th.wallhaven.cc/small/8o/8orrm2.jpg', 'https://th.wallhaven.cc/small/rr/rrd5pj.jpg', 'https://th.wallhaven.cc/small/1p/1pkw2g.jpg', 'https://th.wallhaven.cc/small/x8/x87kw3.jpg', 'https://th.wallhaven.cc/small/p9/p9kv73.jpg', 'https://th.wallhaven.cc/small/wq/wq63wp.jpg', 'https://th.wallhaven.cc/small/p2/p2egej.jpg', 'https://th.wallhaven.cc/small/57/57pl69.jpg', 'https://th.wallhaven.cc/small/p9/p93233.jpg', 'https://th.wallhaven.cc/small/pk/pkrw6p.jpg', 'https://th.wallhaven.cc/small/wy/wy7v8p.jpg', 'https://th.wallhaven.cc/small/l8/l83vjp.jpg', 'https://th.wallhaven.cc/small/7p/7p2ox3.jpg', 'https://th.wallhaven.cc/small/gp/gppvd3.jpg']
#
# def image_link_process(image_link: str) -> str:
#     # https://w.wallhaven.cc/full/rd/wallhaven-rddgwm.jpg
#     # https://th.wallhaven.cc/small/rd/rddgwm.jpg
#     if "small" in image_link:
#         image_link = image_link.replace("th", "w")
#         image_link = image_link.replace("small", "full")
#         url_path = image_link.split("/")
#         url_path[-1] = f"wallhaven-{url_path[-1]}"
#         return "/".join(url_path)
#
#
#
# if __name__ == '__main__':
#     list1 = []
#     pool = Pool(4)
#     for small_link in small_list:
#         list1.append(pool.apply_async(image_link_process, args=(small_link,)))
#     pool.close()
#     for val in list1:
#         print(val.get())
#     print('用时%.2f秒' % (time.time() - start_time))
# 多进程分配任务
# 假设用户需要下载57张图片，进程数是4进程，那么每个进程的任务量是14张，但是还剩一张图片没有下载，那么就需要设计，然最先完成任务的进程去下载这多出来的图片
# 也就是说哪个进程先完成任务谁就执行，并不固定是哪个进程
# 又或者让主进程来完成任务

# 进程数：4，分别完成任务，并将最先完成任务的进程的pid输出





# 1.根据用户输入的图片数量获取小图片链接
# 2.调用类之后执行所有的操作，不需要额外去写函数调用

# 为什么使用类，因为如果使用多个函数的话他们的形参大多相同，如果使用少量函数的话功能有太多，后期不容易维护

# 根据用户需求的图片爬取指定数量的小图片链接，一页小图片链接为24张

# count = 0
# num / 24 + 1(如果余数大于0)
# while 1:
#     num = int(input('>>>'))
#     mod = num % 24
#     quotient = num // 24
#     if mod > 0:
#         count = quotient
#     else:
#         count = quotient - 1
#     print(f'用户最少需要额外爬取{count}页的图片')
#     # 当count等于0是不需要额外进行爬取的，>0则表示需要额外爬取的页数

