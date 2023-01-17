import requests
from lxml import etree
from color import warning

def count(str1: str):  # 用来筛选那个搜索结果的
    for char in str1:
        if char == ' ':
            return str1.index(char)


def search_result(tag:str):
    h1_xpath = '//*[@id="main"]/header/h1/text()'   # 搜索结果的xpath路径
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.447'
                      '2.114 Safari/537.36',
        'referer': 'https://wallhaven.cc/'}
    url = f'https://wallhaven.cc/search?q={tag}&categories=111&purity=110&sorting=relevance&order=desc'
    # sorting表示程度，由于没有放入cookie，所以不开启第三项
    try:
        resp = requests.get(url, headers=header, timeout=5)
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
        warning('搜索标签超时！')
        return False        # 如果是因为响应超时，那么这里直接结束

    html = resp.text
    e = etree.HTML(html)
    text = e.xpath(h1_xpath)[0]
    resp.close()        # 断开连接
    if text[0] == '0':  # 这里需要注意，它是字符0
        print('搜索不到结果')
        return False
    else:
        print(f"{text} \"{tag}\"")
        return True


if __name__ == '__main__':
    search_result('One Piece')
