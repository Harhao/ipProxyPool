__author__ = 'Administrator'
# 操作主要有关的数据库
import pymongo
from settings import *
class mongoOperate(object):
    def __init__(self,MONGO_URI,MONGO_DB,MONGO_USER,MONGO_PASS,MONGO_PORT,COLLECTION_NAME):
        self.mongo_uri=MONGO_URI
        self.mongo_user=MONGO_USER
        self.mongo_db=MONGO_DB
        self.mongo_port=MONGO_PORT
        self.mongo_pass=MONGO_PASS
        self.collectionName=COLLECTION_NAME
    def connect(self,collectionName):
        client=pymongo.MongoClient(hoat=self.mongo_uri,port=self.mongo_port)
        db=client[self.mongo_db]
        db.authenticate(self.mongo_user,self.mongo_pass)
        self.collection=db[self.collectionName]
    def insertData(self,data):
        return self.collection.insert(data)
    def find_one_Data(self,data):
        return self.collection.find_one({})
    def updateData(self,condition,data):
        return self.collection.update(condition,data)
    def removeData(self,condition):
        return self.collection.remove(condition)