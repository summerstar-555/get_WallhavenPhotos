from urllib import response

import requests
from lxml import etree
import time
from search_result import search_result
import os
from multiprocessing import Process, Pool, Value
from random import randint
from color import warning


def print_tags():  # 输出标签
    url = 'https://wallhaven.cc/'
    tags_xpath = '//a[@class="tagname sfw"]/text()'
    try:
        resp = requests.get(url, headers=rand_ua(), timeout=5)
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
        warning('输出标签超时！')
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


def write_pic(tag: str, fullpic_resp, n) -> None:  # 将图片的内容写入
    is_dir(tag)  # 判断目录是否存在
    n.value = n.value + 1  # 写入时将下载成功的次数加上
    print(f'下载成功({n.value})')
    list1 = ['\\', '/', ':', '*', '?', '\"', '<', '>', '\'']  # 违规字符
    for char in tag:
        if char in list1:  # 如果tag标签内有违规字符，那么替换成空格。并且因为这是函数内部，所以并不会对外面的tag造成影响
            tag = tag.replace(char, ' ')
    with open(f'./Pictures/{tag}/%s.jpg' % time.time(), 'wb') as f:  # 使用时间戳命名
        f.write(fullpic_resp.content)


def again(fail_link: str, status_code: int) -> response:            # 重新下载
    if status_code == 404:  # 有可能是大小图片的后缀不同导致404，因此修改再进行尝试，为节省资源，只尝试一次
        fail_link = fail_link.replace('jpg', 'png')  # 将jpg的后缀替换为png
        try:
            resp = requests.get(fail_link, headers=rand_ua())
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):  # 如果五秒内没有响应，那么输出连接超时
            warning('图片重新下载失败！')

        # 成功则返回对应链接的response，失败返回空值
        if resp.status_code != 200:
            warning('图片重新下载失败！')
            return None
        else:
            return resp


def download_pictures(page_num_fuc: int, tag: str, n):  # 一页一页地下载，一页有24张图片
    """
    :param n:
    :param page_num_fuc: 要下载的页面页码
    :param tag: 要搜索的内容标签
    :param header_fuc: 函数内部的http头
    :return: 无返回值
    """
    url = f'https://wallhaven.cc/search?q={tag}&page={page_num_fuc}'
    #       https://wallhaven.cc/search?q=anime&page=3
    small_xpath = '//img[@alt="loading"]/@data-src'  # 小图片的xpath路径
    fail_count = 0  # 下载失败的图片数量
    fail_list = []  # 下载失败的图片链接
    headers = rand_ua()  # 调用随机生成ua的函数
    m = 0  # 循环条件

    while 1:  # 尝试三次，如果还是没响应就退出循环
        try:
            r = requests.get(url, timeout=10, headers=headers)
            break  # 成功连接则退出循环
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):  # 如果五秒内没有响应，那么输出连接超时
            print('连接超时，无法返回网页的响应！')
            m = m + 1
            if m == 3:
                print(f'连接网页失败，第{page_num_fuc}页的进程退出')
                exit(0)  # 直接终止进程
    e = etree.HTML(r.text)
    r.close()

    small_list = e.xpath(small_xpath)  # 获取一页小图片的链接并放在列表中


    for link in small_list:
        full_pic = image_link_process(link)  # 全屏壁纸的链接
        try:
            fullpic_resp = requests.get(full_pic, timeout=5)
        except (requests.exceptions.ConnectTimeout, requests.exceptions.Timeout):
            warning('连接网页超时')
            continue  # 跳过这一张图片的下载

        # 连接失败时：
        if not fullpic_resp.status_code == 200:
            fail_count = fail_count + 1
            print(f"找不到图片！({fail_count})")
            fail_list.append((full_pic, fullpic_resp.status_code))  # 将url以及状态码以元组形式存放
        # 连接成功时：
        else:
            write_pic(tag, fullpic_resp, n)
    if len(fail_list) != 0:
        print('图片重新下载中……')
        for fail_link in fail_list:
            resp_again = again(fail_link[0], fail_link[1])
            if not resp_again:      # 如果返回的不是空值，那么
                write_pic(tag, resp_again, n)
                fail_list.remove(fail_link)
    print(f"第{page_num_fuc}页一共下载了{n.value}张图片，下载失败的图片一共有{fail_count}张")
    print(f'下载失败的图片链接：{fail_list}')


def main(tag1):     # 主函数
    if __name__ == '__main__':
        start_time = time.time()  # 程序的运行开始时间
        process_count = 2  # 进程数量，可指定，进程数量决定下载页数
        star_pagenum = 1  # 下载起始页
        processes = []  # 将生成的进程对象放进此列表中
        n = Value('i', 0)  # 创建共享内存对象，在多进程中需要一个使用同一个变量

        for page_num in range(star_pagenum, process_count + star_pagenum):  # 下载总页数等于进程数，一个进程下载一页的图片
            processes.append(Process(target=download_pictures, args=(page_num, tag1, n)))

        # 让所有子进程开始运行
        for process in processes:
            process.start()
        # 让主进程阻塞等待所有子进程完成
        for process in processes:
            process.join()

        print(f'一共用时%.2f秒,一共下载了{n.value}张' % (time.time() - start_time))


#
#     print_tags()  # 输出标签
#     tag1 = input("\n请输入想搜索的内容标签：")
#     # 从这里开始显示查找标签的结果
#     if not search_result(tag1):  # 调用search_result检查查找的内容是否能查找到结果
#         print('找不到当前结果')
#         exit(0)
#     else:
#         main()


main('wlop')
