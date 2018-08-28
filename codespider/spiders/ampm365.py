#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy
import re
import json


# scrapy crawl ampm365

class TestSpider(scrapy.Spider):
    name = "ampm365"

    #
    def start_requests(self):
        urls = [
            'http://jiameng.ampm365.cn/beside.html'
        ]
        return [scrapy.Request(url=urls[0], callback=self.parse)]

    def parse(self, response):
        store_areas = response.xpath('//select[@id="areas"]/option/@value').extract()

        print(store_areas)

        for store_area in store_areas:
            if not store_area.strip():
                continue
            yield scrapy.Request(
                url="http://yuntuapi.amap.com/datasearch/around?s=rsv3&key=5f0415ee69d818ee8b3f36163475735e&extensions=all&language=en&enc=utf-8&output=jsonp&autoFitView=true&panel=panel&keywords=%e5%ba%97&filter=undefined&sortrule=_id:1&limit=100&tableid=54fff8c9e4b08a4dcf4f9724&city=%E5%85%A8%E5%9B%BD&center=116.39946,39.907629&radius=10000&callback=jsonp_451665_&platform=JS&logversion=2.0&sdkversion=1.3&appname=http%3A%2F%2Fjiameng.ampm365.cn%2Fbeside.html&csid=BDFC4B70-593C-46BE-AD17-35BE94C5A124",
                callback=self.parse2)

    def parse2(self, response):
        body_jsonp = response.body_as_unicode()

        sub_first_index = body_jsonp.index('(')

        body_jsonp = body_jsonp[sub_first_index + 1:-1]

        if body_jsonp.strip():

            body = json.loads(body_jsonp)

            print("count:"+body["count"])

            store_list = body["datas"]

            print(len(store_list))

            for store in store_list:
                city = store["_city"]
                district = store["_district"]

                name = store["_name"]
                address = store["_address"]
                location = store["_location"]
                store_day = store["_createtime"]

                f = open('/Users/xuxiaoshuo/work/python/codespider/codespider/' + TestSpider.name + '.txt', 'a')
                # r只读，w可写，a追加
                f.write(store_day + "@" + city + "@" + district + "@" + name + "@" + address + "@" + location + '\n')

                f.close()
