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


# scrapy crawl familymart

class TestSpider(scrapy.Spider):
    name = "familymart"
    base_url = "http://www.familymart.com.cn"

    city_dict = {}
    district_dict = {}

    #
    def start_requests(self):
        urls = [
            'http://www.familymart.com.cn/store'
        ]
        return [scrapy.Request(url=urls[0], callback=self.parse)]

    def parse(self, response):
        store_city_ids = response.xpath('//select[@id="storeCity"]/option/@value').extract()
        store_city_names = response.xpath('//select[@id="storeCity"]/option/text()').extract()

        for index in range(len(store_city_ids)):
            if not store_city_ids[index].strip():
                continue

            TestSpider.city_dict[store_city_ids[index]] = store_city_names[index]
            yield scrapy.Request(url=TestSpider.base_url + "/store/AreaListForStreet?cid=" + store_city_ids[index],
                                 callback=self.parse2)

    def parse2(self, response):

        pattern = re.compile(r'cid=[0-9]+')
        match = pattern.search(response.url)

        cid = None
        if match:
            cid = match.group()[4:]

        district_list = json.loads(response.body_as_unicode())

        for district in district_list:
            district_id = district["id"]

            TestSpider.district_dict[cid + "-" + district_id] = district["aname"]

            yield scrapy.FormRequest(url=TestSpider.base_url + "/store/Search",
                                     formdata={'cid': str(cid), 'page': str(1)},
                                     callback=self.parse3)

    def parse3(self, response):
        body = json.loads(response.body_as_unicode())
        store_list = body["mapmsg"]

        for store in store_list:
            delete_flg = store["delete_flg"]

            if delete_flg == "0":
                city = TestSpider.city_dict[store["cid"]]
                district = ""
                try:
                    district = TestSpider.district_dict[store["cid"] + "-" + store["aid"]]
                except KeyError:
                    print(store["cid"] + "-" + store["aid"] + "@" + store["street"])
                name = store["name"]
                address = store["street"]
                lng = store["jd"]
                lat = store["wd"]

                store_day = store["createtime"]

                path = "./" + datetime.datetime.now().strftime('%Y-%m-%d')
                is_exists = os.path.exists(path)

                if not is_exists:
                    os.makedirs(path)

                f = open(path + "/"
                         + datetime.datetime.now().strftime('%Y-%m-%d')
                         + "_" + TestSpider.name + '.txt',
                         'a')  # r只读，w可写，a追加
                f.write(
                    store_day + "@" + city + "@" + district + "@" + name + "@" + address + "@" + lng + "," + lat + '\n')

                f.close()
