# coding=UTF-8
# html解析器
# http://baike.baidu.com/item/Python

from bs4 import BeautifulSoup
import re

class HtmlParser(object):

    def get_new_urls(self, new_url, soup):
        new_urls = set() # 集合
        # 格式是 /item/***
        links = soup.find_all('a', href=re.compile(r'/item/'))
        for link in links:
            url = 'http://baike.baidu.com' + link['href']
            # # url = urlparse.urlparse(new_url, url) # 按照new_url的格式对URL进行拼接 # 这行出了问题！！！
            new_urls.add(url)
        return new_urls


    def get_new_data(self, new_url, soup):
        # 此爬虫拆分出词条的名字和摘要数据
        rest_data = {} # 用字典来存储临时的数据

        # 对URL有存储一下，以便后面的使用
        rest_data['url'] = new_url

        # 这是title的样式
        # <dd class="lemmaWgt-lemmaTitle-title"> <h1>Python</h1>

        title_node = soup.find('dd', class_='lemmaWgt-lemmaTitle-title').find('h1')

        rest_data['title'] = title_node.get_text()

        # 这是summary的样式
        # <div class="lemma-summary" label-module="lemmaSummary">
        summary_node = soup.find('div', class_='lemma-summary')
        rest_data['summary'] = summary_node.get_text()

        return rest_data


    def parse(self, new_url, html_content):

        if new_url is None or html_content is None:
            return

        # 接下来对content进行解析
        soup = BeautifulSoup(html_content, 'html.parser', from_encoding='utf-8')

        new_urls = self.get_new_urls(new_url, soup)
        new_data = self.get_new_data(new_url, soup)

        return new_urls, new_data
