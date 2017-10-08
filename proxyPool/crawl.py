__author__ = 'Administrator'
# 抓取IP的主要逻辑
from urllib import request
import urllib.parse
import logging
from multiprocessing import  pool
from time import sleep
import random
from lxml import etree
def getRandomUserAgnet():
    user_agents=[
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 QIHU 360S"
    ]
    userAgent=random.choice(user_agents)
    return userAgent
def getProxies():
    proxies=[]
    for i in range(1,10):
        url="http://www.xicidaili.com/nn/{0}".format(i)
        userAgent=getRandomUserAgnet()
        headers={"User-Agent":userAgent}
        opener=urllib.request.build_opener()
        opener.addheaders=[headers]
        try:
            data=opener.open(url,timeout=5).read()
            sleep(3)
        except Exception as e:
            logging.debug(e)
        selector=etree.HTML(data)
        ip_addr=selector.xpath("//tr[@class='odd']/td[2]/text()")
        port=selector.xpath("//tr[@class='odd']/td[3]/text()")
        sur_time=selector.xpath("//tr[@class='odd']/td[9]/text()")
        ver_time=selector.xpath("//tr[@class='odd']/td[10]/text()")
        for j in range(len(ip_addr)):
            ip=ip_addr[j]+":"+port[j]
            proxies.append(ip)
    return proxies
def verify_ip(currentIp):
    tmp_proxies=[]
    testUrl="http://www.baidu.com"
    userAgent=getRandomUserAgnet()
    proxy_support=urllib.request.ProxyHandler({"http":currentIp})
    opener=urllib.request.build_opener(proxy_support)
    opener.addheaders=[("User-Agent",userAgent)]
    urllib.request.install_opener(opener)
    try:
        res=urllib.request.urlopen(testUrl,timeout=5).read()
        if len(res)!=0:
            tmp_proxies.append(currentIp)
    except urllib.error.URLError as er2:
        if hasattr(er2,'code'):
            logging.debug("unvalid ipaddress"+currentIp+str(er2.code))
        if hasattr(er2,"reason"):
            logging.debug("reason is the "+currentIp+str(er2.reason))
    except Exception as er:
        logging.debug(er)
    sleep(2)
    return tmp_proxies
if __name__=="__main__":
    getProxies()
