import pymongo
from urllib import request
import urllib.parse
from time import sleep
import logging
import multiprocessing
from .setttings import *
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
        self.client=pymongo.MongoClient(host=self.mongo_uri,port=self.mongo_port)
        self.db=self.client[self.mongo_db]
        self.db.authenticate(self.mongo_user,self.mongo_pass)
    def insertData(self,data):
        return self.db[self.collectionName].insert(data)
    def find_Data(self):
        return self.db[self.collectionName].find({})
    def updateData(self,condition,data):
        return self.db[self.collectionName].update(condition,data)
    def removeData(self,condition):
        return self.db[self.collectionName].remove(condition)
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
            if res.status_code==200:
                return "valid IP"
            else:
                self.db[self.collectionName].remove({'ip_addr': item['ip_addr']})
                return "invalid IP"
        except Exception as e:
            self.db[self.collectionName].remove({'ip_addr': item['ip_addr']})
            return "invalid IP Exception"
def main():
    try:
        mongoObj=mongoOperate(MONGO_URI,MONGO_DATABASE,MONGO_USER,MONGO_PASS,MONGO_PORT,COLLECTION_NAME)
        mongoObj.connect()
        print(mongoObj.find_Data())
        while True:
            ipItems=mongoObj.find_Data()
            if ipItems:
                for ipItem in ipItems:
                    if ipItem:
                        tips=mongoObj.verifyIP(ipItem)
                        print(tips)
                    else:
                        break
            else:
                print("no ip  data!!")
                break
            sleep(5)
    except Exception as e:
        print(e)

if __name__=="__main__":
    print("start verify")
    # p1 = multiprocessing.Process(target=main, args=('test1',))
    # p2 = multiprocessing.Process(target=main, args=('test2',))
    # p3 = multiprocessing.Process(target=main, args=('test3',))
    # p1.start()
    # p2.start()
    # p3.start()
    # p1.join()
    # p2.join()
    # p3.join()
    p=multiprocessing.Pool(4)
    for i in range(5):
        p.apply_async(main, args=(i,))
    p.close()
    p.join()
    print("all proccess is ended")

    
