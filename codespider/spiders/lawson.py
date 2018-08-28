#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import json

import datetime

import os
import scrapy
import re

import time


class TestSpider(scrapy.Spider):
    name = "lawson"

    def start_requests(self):
        urls = [
            'bj-lawson',
            'wh-lawson',
            'dl-lawson',
            'sh-lawson',
            'cq-lawson'
        ]

        base_url = "https://lawsonapp.api.yorentick.cn/app/v1/shop/?page=1&pageSize=15000&upDa=1103249250000&timestamp=1519353121318&nonce=kWJYv8&signature=dc452c95ff33a21c3b33388d39d0b9bd46c4d920&device=1&regionBlockCode="
        for url in urls:
            yield scrapy.Request(url=base_url + url, callback=self.parse)

    def parse(self, response):

        body_json = response.body_as_unicode()

        body = json.loads(body_json)

        store_list = body["data"]["list"]

        print(len(store_list))

        for store in store_list:
            city = store["provinceDistrict"]
            # district = ""

            name = store["shopName"]
            address = store["address"]
            location = str(store["latitude"]) + "," + str(store["longitude"])
            store_day = store["openDate"]

            path = "./" + datetime.datetime.now().strftime('%Y-%m-%d')
            is_exists = os.path.exists(path)

            if not is_exists:
                os.makedirs(path)

            f = open(path + "/"
                     + datetime.datetime.now().strftime('%Y-%m-%d')
                     + "_"
                     + TestSpider.name + '.txt', 'a')
            # r只读，w可写，a追加
            f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(
                store_day / 1000.0)) + "@" + city + "@" + name + "@" + address + "@" + location + '\n')

            f.close()
