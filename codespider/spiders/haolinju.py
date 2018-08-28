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


class TestSpider(scrapy.Spider):
    name = "haolinju"
    base_url = "https://n.e24c.com/ap/store/storedetail/"

    #
    def start_requests(self):
        for num in range(1, 1500):
            yield scrapy.Request(url=TestSpider.base_url + str(num), callback=self.parse)

    def parse(self, response):

        address_table = response.xpath('//div[@class="address"]/table')

        name = address_table.xpath('(./tr)[1]/td/div/text()').extract_first()

        address = address_table.xpath('(./tr)[2]/td/div/text()').extract_first()

        if not name:
            name = ""

        if not address:
            address = ""

        body = response.body_as_unicode()

        pattern_lat = re.compile(r'lat=\'[0-9]+.[0-9]+\'')
        match = pattern_lat.search(body)

        lat = ""
        if match:
            lat = match.group().rstrip().replace("lat=\'", "").replace("\'", "")

        pattern_lng = re.compile(r'lng=\'[0-9]+.[0-9]+\'')
        match = pattern_lng.search(body)

        lng = ""
        if match:
            lng = match.group().rstrip().replace("lng=\'", "").replace("\'", "")

        path = "./" + datetime.datetime.now().strftime('%Y-%m-%d')
        is_exists = os.path.exists(path)

        if not is_exists:
            os.makedirs(path)

        f = open(path + "/"
                 + datetime.datetime.now().strftime('%Y-%m-%d')
                 + "_"
                 + TestSpider.name + '.txt',
                 'a')  # r只读，w可写，a追加
        f.write(name + "@" + address + "@" + lng + "," + lat + '\n')

        f.close()
