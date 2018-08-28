#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import datetime

import os
import scrapy
import json
import time


# scrapy crawl ampm365

class TestSpider(scrapy.Spider):
    name = "linjia"

    #
    def start_requests(self):
        urls = [
            'http://api.map.baidu.com/geosearch/v3/nearby?ak=4CY8uFTiLuqnKAHGPkDK1doB5n6H62eq&coord_type=3&sortby=distance:1&radius=3000000&page_index=0&page_size=1000&geotable_id=151390&location=116.396795,39.927552'
        ]
        return [scrapy.Request(url=urls[0], callback=self.parse)]

    def parse(self, response):
        body_json = response.body_as_unicode()

        body = json.loads(body_json)

        store_list = body["contents"]

        print(len(store_list))

        for store in store_list:
            city = store["province"]
            district = store["district"]

            name = store["mallName"]
            address = store["address"]
            location = str(store["location"][0]) + "," + str(store["location"][1])
            store_day = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(store["create_time"]))

            path = "./" + datetime.datetime.now().strftime('%Y-%m-%d')
            is_exists = os.path.exists(path)

            if not is_exists:
                os.makedirs(path)

            f = open(path + "/"
                     + datetime.datetime.now().strftime('%Y-%m-%d')
                     + "_"
                     + TestSpider.name + '.txt', 'a')
            # r只读，w可写，a追加
            f.write(store_day + "@" + city + "@" + district + "@" + name + "@" + address + "@" + location + '\n')

            f.close()
