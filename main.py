import multiprocessing
import re
from socket import socket
from urllib import response

import requests
from lxml import etree
import time
from search_result import search_result
import os
from multiprocessing import Process, Pool, Value
import multiprocessing.sharedctypes
from random import randint
from color import warning


def print_tags():  # 输出wallhaven首页的标签
    url = 'https://wallhaven.cc/'
    tags_xpath = '//a[@class="tagname sfw"]/text()'
    try:
        resp = requests.get(url, headers=rand_ua(), timeout=5)
    except Exception as e:
        warning(f'{e}')
        return False  # 如果是因为响应超时，那么这里直接结束
    element = etree.HTML(resp.text)
    list1 = element.xpath(tags_xpath)
    resp.close()
    for tag_content in list1:
        tag_content = '#' + tag_content
        print(f"\033[0;36;40m{tag_content}\033[0m", end='  ')  # 改变字体的前景色和背景色


def rand_ua():
    # ua列表
    user_agent_list = [
        'Mozilla/5.0 (WindowsNT6.1;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/39.0.2171.95Safari/537.36OPR/26.0.16'
        '56.60',
        'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/53'
        '7.36',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Sa'
        'fari/534.50',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.'
        '50',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safar'
        'i/535.11',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.3'
        '6 Edg/108.0.1462.76'
    ]
    rand_num = randint(0, len(user_agent_list) - 1)  # 随机数从0开始，列表总数-1结束
    header_fuc = {
        'user-agent': user_agent_list[rand_num],  # 每次都生成随机的UA
    }
    return header_fuc

def is_dir(tag: str):
    if not os.path.exists('./Pictures'):
        print('跟目录下创建文件夹Pictures')
        os.mkdir('./Pictures')

    list1 = ['\\', '/', ':', '*', '?', '\"', '<', '>', '\'']  # 违规字符
    for char in tag:
        if char in list1:  # 如果tag标签内有违规字符，那么替换成空格。并且因为这是函数内部，所以并不会对外面的tag造成影响
            tag = tag.replace(char, ' ')
    pic_path = f'./Pictures/{tag}/'  # 根据用户输入的标签进行创建文件夹

    if not os.path.exists(pic_path):  # 检查是否存在
        print(f'在根目录下创建文件夹{pic_path}')
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





def again(fail_link: str) -> response:            # 重新下载
    # 针对404错误的重试
    """
    :param fail_link: 下载失败的图片链接
    :return: 成功则返回response对象，失败则返回空
    """
    fail_link = fail_link.replace('jpg', 'png')  # 将jpg的后缀替换为png
    try:
        resp = requests.get(fail_link, headers=rand_ua(), timeout=5)
    except Exception as e:
        warning(f'{e}')
        return None

    # 成功则返回对应链接的response，失败返回空值
    if resp.status_code != 200:
        warning('图片重新下载失败！')
        return None
    else:
        return resp





    # 4进程
    # processes_count = 4     # 进程数
    # processes = [Process(target=multiprocess_download, args=(small_list, i, len(small_list) / processes_count)) for i in range(processes_count)]
    #
    # for process in processes:
    #     process.start()
    #
    # for process in processes:
    #     process.join()

    # if __name__ == '__main__':
    #     processes_count = 4  # 进程数
    #     pool = Pool(processes_count)
    #     for small_link in small_list:
    #         pool.apply_async(multiprocess_download, args=small_link)
    #     pool.close()
    #     pool.join()
    #
    #
    # print('Download finish!')
    # if fail_count != 0:     # 如果下载失败的图片数量非0
    #     print('图片重新下载中……')
    #     for fail_link in fail_list:
    #         resp_again = again(fail_link[0], fail_link[1])
    #         if not resp_again is None:      # 如果这里函数返回的不是空值，也就是一个response对象，那么执行
    #             write_pic(tag, resp_again, share)
    #
    #             fail_list.remove(fail_link)
    #             fail_count = len(fail_list)  # 下载失败的图片数量
    #
    # # 输出结果
    # print(f"第{page_num_fuc}页一共下载了{share.value}张图片，下载失败的图片一共有{fail_count}张")
    # print(f'下载失败的图片链接：{fail_list}')

class DownloadPicture:
    def __init__(self, tag: str = None,pic_count: int = 1, success_count: int = 4):
        """
        :param tag: 用户想要搜索的图片标签
        :param pic_count: 想要下载的图片数量，默认为1，为0则无意义
        :param share_obj: 共享对象，用于多进程共享内存
        :param success_count:进程数，默认4进程
        """
        self.tag = tag
        self.share_obj = Value('i', 0)
        self.pic_count = pic_count
        self.success_count = success_count

        # 自动调用方法
        resp = self.search_result()
        if not resp is None:
            self.small_list = self.get_small_list(resp)
            self.multiprocess_download()


    def get_response(self, page_num = 1):
        url = f'https://wallhaven.cc/search?q={self.tag}&categories=111&purity=110&sorting=relevance&order=desc&page={page_num}'
        header = rand_ua()
        try:
            resp = requests.get(url, headers=header, timeout=5)
            return resp
        except Exception as e:     # 如果是请求是异常再捕获
            warning(e)
            return None  # 如果是因为响应超时，那么这里直接结束
    def search_result(self):
        h1_xpath = '//*[@id="main"]/header/h1/text()'  # 搜索结果的xpath路径
        resp = self.get_response()      # 调用响应函数
        html = resp.text
        e = etree.HTML(html)
        text = e.xpath(h1_xpath)[0]
        if text[0] == '0':  # 这里需要注意，它是字符0
            print('搜索不到结果')
            resp.close()  # 看情况断开连接
            return None
        else:
            print(f"\n{text} \"{self.tag}\"")     # 这里需要拼接，因为wallhaven本身搜索结果也是拼接的
            return resp         # 成功返回response

    def get_small_list(self, resp: response) -> list:  # 返回小图片列表
        small_list = []
        mod = self.pic_count % 24   # 余数
        quotient = self.pic_count // 24 # 商
        small_xpath = '//img[@alt="loading"]/@data-src'  # 小图片的xpath路径

        if mod > 0:
            count = quotient        # count是需要额外爬取的页数
        else:
            count = quotient - 1

        # 将商等于0的按照余数进行下载并放到列表中，将商大于0的进行一页页的下载，再将余数进行单独下载
        html = resp.text
        e = etree.HTML(html)
        small_list = e.xpath(small_xpath)
        if count > 0:
            for i in range(2, count + 2):   # 需要额外下载的页数
                resp = self.get_response(i)
                if not resp is None:
                    html = resp.text
                    e = etree.HTML(html)
                    small_list.extend(e.xpath(small_xpath))     # 向列表内追加另一个列表中的所有元素
                resp.close()

        return small_list

    def write_pic(self, full_pic_resp: response) -> None:  # 将图片的内容写入
        is_dir(self.tag)  # 判断目录是否存在
        self.share_obj.value = self.share_obj.value + 1  # 写入时将下载成功的次数加上
        print(f'下载成功({self.share_obj.value})')
        list1 = ['\\', '/', ':', '*', '?', '\"', '<', '>', '\'']  # 违规字符
        for char in self.tag:
            if char in list1:  # 如果标签内有违规字符，那么替换成空格。并且因为这是函数内部，所以并不会对外面的self.tag造成影响
                self.tag = self.tag.replace(char, ' ')
        with open(f'./Pictures/{self.tag}/%s.jpg' % time.time(), 'wb') as f:  # 使用时间戳命名
            f.write(full_pic_resp.content)

    def multiprocess_download(self):
        fail_list = []  # 下载失败的图片链接
        fail_count = len(fail_list)  # 下载失败的图片数量

        for i in range(self.pic_count):
            full_pic_link = image_link_process(self.small_list[i])  # 将小图片的链接转换为全屏壁纸的链接

            # 转换之后向服务器进行校验
            try:
                full_pic_resp = requests.get(full_pic_link, timeout=5)
            except Exception as e:
                warning(f'{e}')
                continue  # 跳过这一张图片的下载

            # 对状态码进行判断：
            if full_pic_resp.status_code == 404:
                print('图片下载失败，重新下载中……')
                resp = again(full_pic_link)
                if not resp is None:
                    self.write_pic(full_pic_resp)
            elif full_pic_resp.status_code == 200:
                self.write_pic(full_pic_resp)

            else:
                fail_list.append((full_pic_link, full_pic_resp.status_code))  # 将url以及状态码以元组形式存放
                fail_count = len(fail_list)  # 下载失败的图片数量
                print(f"找不到图片！({fail_count})")

            full_pic_resp.close()  # 无论连接是否成功，都要断开连接


# def main(tag1):     # 主函数
#     if __name__ == '__main__':
#         start_time = time.time()  # 程序的运行开始时间
#         process_count = 2  # 进程数量，可指定，进程数量决定下载页数
#         star_pagenum = 1  # 下载起始页
#         processes = []  # 将生成的进程对象放进此列表中
#         share = Value('i', 0)  # 创建共享内存对象，在多进程中需要一个使用同一个变量
#
#         for page_num in range(star_pagenum, process_count + star_pagenum):  # 下载总页数等于进程数，一个进程下载一页的图片
#             processes.append(Process(target=get_small_list, args=(page_num, tag1, share)))
#
#         # 让所有子进程开始运行
#         for process in processes:
#             process.start()
#         # 让主进程阻塞等待所有子进程完成
#         for process in processes:
#             process.join()
#
#         print(f'一共用时%.2f秒,一共下载了{share.value}张' % (time.time() - start_time))


# print_tags()  # 输出标签
# tag = input("请输入想搜索的内容标签：")
# share = Value('i', 1)
# class1 = DownloadPicture(tag, 11, share)
# # 从这里开始显示查找标签的结果
# if not class1.search_result():  # 调用search_result检查查找的内容是否能查找到结果
#     print('找不到当前结果')
#     exit(0)
# else:
#     print('进入主程序')
#     # main()
obj1 = DownloadPicture(tag='4k', pic_count=25)





