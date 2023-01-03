import requests
from lxml import etree


def count(str1: str):  # 用来筛选那个搜索结果的
    for char in str1:
        if char == ' ':
            return str1.index(char)


def search_result(tag:str):
    h1_xpath = '//*[@id="main"]/header/h1/text()'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                      ' (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54'
    }
    url = f'https://wallhaven.cc/search?q={tag}' \
          f'&categories=110&purity=110&sorting=relevance&order=desc'  # 这个是用来控制纯度的，110代表前两项都开启
    html = requests.get(url, headers=headers).text
    e = etree.HTML(html)
    text = e.xpath(h1_xpath)[0]
    if text[0] == '0':  # 这里需要注意，它是字符0
        print('搜索不到结果')
        return False
    else:
        print(f"{text} \"{tag}\"")
        return True


if __name__ == '__main__':
    search_result('wlop')
