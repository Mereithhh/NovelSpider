# NovelSpider
基于scrapy的小说爬虫：爬取笔趣阁的制定小说并下载到txt，速度很快哦。

## 前言

最近一直在学爬虫，从最基本的`urllib`到`requests`、`beautifulsoup`到分布式爬虫框架`scrapy`,现在终于感觉可以上路了。所以先基于`scrapy`重写了我以前做的小说爬虫，代码都很简单，就不注释了。相关的知识点在我的python爬虫系列文章后面都会介绍到。
主要的参考文献：
> * [scrapy官方文档(无中文)](https://docs.scrapy.org/en/latest/)
> * [python官方文档(有中文)](https://docs.python.org/zh-cn/3/)

## 思路

> 1.搜索小说名，用`requests+lxml`爬取结果，并让用户选择结果，返回小说目录的`url`
> 2.`scrapy`根据目录url解析小说章节数以及每章的具体url，其中把小说章节数送给`item`再到`itempipeline`保存，每章的url则是生成异步请求，结果送给`parse_chapter`进行下一步的解析
> 3.`parse_chapter`解析每一章的内容，替换没用的`\xa0`，写入到`item`里，返回交给`pipeline`处理
> 4.对于`pipeline`为了写入文件章节顺序是对的，每次返回的`item`都先保存到包括当前章节`编号和内容`的字典里
> 5.爬取完毕，对字典进行排序，写入到小说文件中

## 使用说明
### 依赖
需要安装：
> scrapy
> requests

直接`pip instal scrapy requests`即可，如果`scrapy`安装不了需要编译没成功的话，那么到[这个网站](http://www.lfd.uci.edu/~gohlke/pythonlibs/)下载自己对应编译好的再用pip安装即可

### 运行
在`项目目录`中打开`shell`运行
```shell
scrapy crawl xiaoshuo -a name=小说名 --nolog
```
