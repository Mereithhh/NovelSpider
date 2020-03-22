import scrapy
from xiaoshuo.items import XiaoshuoItem
import requests
from lxml import etree
from urllib import parse
import sys

def search(name):
    print('小说搜索：{}'.format(name))
    print("***********************")
    if not name:
        print('请输入要搜索的小说名后再试！')
        sys.exit()
    search_url = r'https://www.biquge.com.cn/search.php?q=' + parse.quote(name)
    headers = {'user-agent': r'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
    res = requests.get(search_url,headers=headers)
    res.encoding = 'utf-8'
    html = etree.HTML(res.text)
    r = html.xpath(r'//div[@class="result-list"]/div')
    if not r:
        print('没有结果，请重试！')
        sys.exit()
    n = len(r)
    print('一共有{}个结果，分别是：'.format(n))
    for i in range(n):
        name = r[i].xpath(r'./div/h3/a/span/text()')[0]
        author = r[i].xpath(r'./div/div/p/span[2]/text()[1]')[0]
        typ = r[i].xpath(r'./div/div/p/span[2]/text()[1]')[1]
        print('{}:{}     作者：{}    类型：{}'.format(i+1,name,author,typ))
    print('*****************')
    chose = input('你的选择是：')
    if int(chose) <= n:
        url = r'https://www.biquge.com.cn' + r[int(chose)-1].xpath(r'./div/a[@cpos="img"]/@href')[0]
        return url
    else:
        print('输入错误，请重试！')


class xiaoshuo(scrapy.Spider):

    name = 'xiaoshuo'
    start_urls = []

    def __init__(self, name='修真聊天群', *args, **kwargs):
        super(xiaoshuo, self).__init__(*args, **kwargs)
        self.start_urls.append(search(name))


    def parse(self,response):
        item = XiaoshuoItem()
        #from scrapy.shell import inspect_response
        #inspect_response(response, self)
        item['novel_name']= response.css('h1::text').get()
        chapters = response.xpath(r'//div[@id="list"]/dl/dd/a')
        item['lenn'] = len(chapters)
        yield item
        for i in range(len(chapters)):
            url = r'https://www.biquge.com.cn' + chapters[i].xpath(r'@href').get()
            yield scrapy.Request(url,callback=self.parse_chapter,cb_kwargs={'ids':i})
        



    def parse_chapter(self,response,ids):
        item = XiaoshuoItem()
        item['num'] = ids
        texts = response.xpath(r"//div[@id='content']/text()").getall()
        chapter_name = response.css(r"div.bookname h1::text").get()
        text = chapter_name + '\n\n'
        for line in texts:
            text = text +  '  ' + line.replace('\xa0\xa0\xa0\xa0','') + '\n'
        text = text + '\n\n'
        item['text'] = text
        yield item




