__author__ = 'Administrator'
# 操作主要有关的数据库
import pymongo
from urllib import request
import urllib.parse
from time import sleep
import logging
MONGO_URI=''
MONGO_DATABASE=''
MONGO_USER=""
MONGO_PASS=""
MONGO_PORT=
COLLECTION_NAME="ipProxy"
class mongoOperate(object):
    def __init__(self,MONGO_URI,MONGO_DB,MONGO_USER,MONGO_PASS,MONGO_PORT,COLLECTION_NAME):
        self.mongo_uri=MONGO_URI
        self.mongo_user=MONGO_USER
        self.mongo_db=MONGO_DB
        self.mongo_port=MONGO_PORT
        self.mongo_pass=MONGO_PASS
        self.collectionName=COLLECTION_NAME
    def connect(self):
        client=pymongo.MongoClient(host=self.mongo_uri,port=self.mongo_port)
        db=client[self.mongo_db]
        db.authenticate(self.mongo_user,self.mongo_pass)
        self.collection=db[self.collectionName]
    def insertData(self,data):
        return self.collection.insert(data)
    def find_Data(self):
        return self.collection.find({})
    def updateData(self,condition,data):
        return self.collection.update(condition,data)
    def removeData(self,condition):
        return self.collection.remove(condition)
    def verifyIP(self,item):
        ip=item["wholeIP"]
        testUrl="http://www.baidu.com"
        userAgent='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        proxy_support=urllib.request.ProxyHandler({"http":ip})
        opener=urllib.request.build_opener(proxy_support)
        opener.addheaders=[("User-Agent",userAgent)]
        urllib.request.install_opener(opener)
        try:
            res=urllib.request.urlopen(testUrl,timeout=5).read()
            if len(res)==0:
                self.db[self.collection_name].remove({'ip_addr': item['ip_addr']})
        except Exception as e:
            logging.debug(e)
if __name__=="__main__":
    mongoObj=mongoOperate(MONGO_URI,MONGO_DATABASE,MONGO_USER,MONGO_PASS,MONGO_PORT,COLLECTION_NAME)
    mongoObj.connect()
    while True:
        ipItems=mongoObj.find_Data()
        for ipItem in ipItems:
            if ipItem:
                mongoObj.verifyIP(ipItem)
                logging.info("verifying......")
            else:
                break
        sleep(10)

