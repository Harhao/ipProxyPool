# -*- coding: utf-8 -*-
import logging
from scrapy import Request,Spider
from time import  sleep
from ipProxyPool.items import IpproxypoolItem
class CrawlipSpider(Spider):
    name = "crawlIP"
    allowed_domains = ["www.xicidai.com"]
    start_urls = ['http://www.xicidaili.com/nn/']

    def parse(self, response):
        # lastPageNum=response.xpath("//*[@id='body']/div[2]/a[10]/text()").extract_first()
        # lastPageNum=int(lastPageNum)
        for i in range(1062):
            num=i+1
            sleep(2)
            yield Request(url=response.url+str(num),callback=self.parse_info,dont_filter=True)

    def parse_info(self,response):
        tables=response.xpath('//*[@id="ip_list"]')[0]
        trs=tables.xpath("//tr")[1:]
        for i in range(len(trs)):
            tr=trs[i]
            item=IpproxypoolItem()
            item["ip_addr"]=tr.xpath(".//td[2]/text()").extract_first()
            item["port"]=trs[i].xpath(".//td[3]/text()").extract_first()
            item["location"]=trs[i].xpath(".//td[4]/a/text()").extract_first()
            item["type"]=trs[i].xpath(".//td[5]/text()").extract_first()
            item["netType"]=trs[i].xpath(".//td[6]/text()").extract_first()
            item["speed"]=trs[i].xpath(".//td[7]/div/@title").extract_first()
            item["connTime"]=trs[i].xpath(".//td[8]/div/@title").extract_first()
            item["aliveTime"]=trs[i].xpath(".//td[9]/text()").extract_first()
            item["verifyTime"]=trs[i].xpath(".//td[10]/text()").extract_first()
            item["wholeIP"]=str(item['netType'])+'://'+str(item['ip_addr'])+':'+str(item['port'])
            # self.state["items_count"]=self.state.get("items_count",0)+1
            yield item