# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import pymongo
from urllib import request
import urllib.parse
class IpproxypoolPipeline(object):
    collection_name="ipProxy"
    def __init__(self,mongo_uri,mongo_db,mongo_user,mongo_pass):
        self.mongo_uri=mongo_uri
        self.mongo_db=mongo_db
        self.mongo_user=mongo_user
        self.mongo_pass=mongo_pass
    @classmethod
    def from_crawler(cls,crawler):
        return cls(mongo_uri=crawler.settings.get('MONGO_URI'),mongo_db=crawler.settings.get('MONGO_DATABASE'),mongo_user=crawler.settings.get("MONGO_USER"),mongo_pass=crawler.settings.get("MONGO_PASS"))
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.db.authenticate(self.mongo_user,self.mongo_pass)

    def close_spider(self, spider):
        self.client.close()
    def process_item(self, item, spider):
        # self.verifyIP(item)
        self.db[self.collection_name].insert(dict(item))
        return item
    # def verifyIP(self,item):
    #     ip=item["wholeIP"]
    #     testUrl="http://www.baidu.com"
    #     userAgent='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    #     proxy_support=urllib.request.ProxyHandler({"http":ip})
    #     opener=urllib.request.build_opener(proxy_support)
    #     opener.addheaders=[("User-Agent",userAgent)]
    #     urllib.request.install_opener(opener)
    #     try:
    #         res=urllib.request.urlopen(testUrl,timeout=5).read()
    #         if len(res)!=0:
    #             #self.db[self.collection_name].update({'ip_addr': item['ip_addr']}, {'$set': dict(item)}, True)
    #             self.db[self.collection_name].insert(dict(item))
    #             return item
    #         else:
    #             return False
    #     except Exception as e:
    #         logging.debug(e)
