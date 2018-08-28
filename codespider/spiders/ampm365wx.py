#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import datetime

import os
import scrapy
import re
import json


# scrapy crawl ampm365

class TestSpider(scrapy.Spider):
    name = "ampm365wx"

    #
    def start_requests(self):
        urls = [
            'http://wechat.ampm365.cn/org/business/PS100011.do'
        ]
        return [scrapy.FormRequest(url=urls[0],
                                   headers={'tokenPassword': '1qaz2wsx', 'developToken': '000006'},
                                   formdata={'currentPageNum': str(1), 'pageCount': str(20000)},
                                   callback=self.parse)]

    def parse(self, response):
        body_json = response.body_as_unicode()

        body = json.loads(body_json)

        store_list = body["result"]["list"]

        print(len(store_list))

        for store in store_list:
            # city = store["_city"]
            # district = store["_district"]

            name = store["shopName"]
            address = store["entity"]["address"]
            location = str(store["location"][0]) + ',' + str(store["location"][1])
            store_day = store["entity"]["createTimeCh"]

            path = "./" + datetime.datetime.now().strftime('%Y-%m-%d')
            is_exists = os.path.exists(path)

            if not is_exists:
                os.makedirs(path)

            f = open(path + "/"
                     + datetime.datetime.now().strftime('%Y-%m-%d')
                     + "_" + TestSpider.name + '.txt', 'a')
            # r只读，w可写，a追加
            # f.write(store_day + "@" + city + "@" + district + "@" + name + "@" + address + "@" + location + '\n')
            f.write(store_day + "@" + name + "@" + address + "@" + location + '\n')

            f.close()
