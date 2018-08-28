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
    name = "711bj"
    base_url = "http://7-11bj.com.cn"

    #
    def start_requests(self):
        urls = [
            'http://7-11bj.com.cn/?store.html'
        ]
        return [scrapy.Request(url=urls[0], callback=self.parse)]

    def parse(self, response):
        page_subtitle = response.xpath('//h4[@class="pageSubtitle"]/text()').extract()
        shop_list = response.xpath('//div[@class="shopList"]')
        item_urls = shop_list.xpath('.//a/@href').extract()
        print(len(item_urls))

        for item_url in item_urls:
            yield scrapy.Request(url=TestSpider.base_url + item_url[1:], callback=self.parse2)

    def parse2(self, response):
        store_tbl = response.xpath('//div[@class="storeTbl"]')
        item_urls = store_tbl.xpath('.//a/@href').extract()
        print(len(item_urls))

        for item_url in item_urls:
            yield scrapy.Request(url=TestSpider.base_url + item_url[1:], callback=self.parse3)

    def parse3(self, response):
        address = response.xpath('//h4[@class="pageSubtitle"]/text()').extract_first()

        store_tbl = response.xpath('//div/table')

        location = store_tbl.xpath('(./tr)[1]/td/text()').extract_first()

        store_day = store_tbl.xpath('(./tr)[4]/td/text()').extract_first()

        map_point = None

        pattern = re.compile(r'BMap.Point\([\s\S]*?\)')
        match = pattern.search(response.body_as_unicode())

        if match:
            map_point = match.group()[11:-1]

        path = "./" + datetime.datetime.now().strftime('%Y-%m-%d')
        is_exists = os.path.exists(path)

        if not is_exists:
            os.makedirs(path)

        f = open(path + "/"
                 + datetime.datetime.now().strftime('%Y-%m-%d')
                 + "_"
                 + TestSpider.name + '.txt',
                 'a')  # r只读，w可写，a追加
        f.write(store_day + "@" + address + "@" + location + "@" + map_point + '\n')

        f.close()
