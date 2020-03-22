# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import sys
import os

class XiaoshuoPipeline(object):
    counter = 0
    text_cache = {}
    all_n = 0


    def process_item(self, item, spider):
        if  'text' in item :
            self.text_cache[item['num']] = item['text']
            self.counter = self.counter+1
            sys.stdout.write('{} / {}'.format(self.counter,self.all_n) + '\r')
            sys.stdout.flush()
            return item
        else:
            self.all_n = int(item['lenn'])
            self.novel_name = item['novel_name'] + r'.txt'
            self.f = open(self.novel_name,'wb')
            return item           

    def close_spider(self,spider):
        sorted_text = sorted(self.text_cache.items(),key=lambda item:item[0])
        for line in sorted_text:
            self.f.write(line[1].encode('utf-8'))
        self.f.close()
        print('小说成功下载到：{}/{}'.format(os.getcwd(),self.novel_name))