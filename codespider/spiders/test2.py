#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import urllib

import scrapy
import json
import time

from PIL import Image
# from StringIO import StringIO
from scrapy import FormRequest, Request

from scrapy.exceptions import CloseSpider


class TestSpider(scrapy.Spider):
    name = "test2"
    allowed_domains = ["baic.gov.cn"]

    current_cookies = None

    current = ""

    image_url = ""

    #
    def start_requests(self):
        TestSpider.current_cookies = [{'name': 'JSESSIONID',
                                       'value': 'Fj0u2HZE74BCSLWKXg92DaGXDktoC2LQ8ba6I6F_hhLjkcB3SnWb!200258832',
                                       'domain': 'qyxy.baic.gov.cn',
                                       'path': '/'},
                                      {'name': 'CNZZDATA1257386840',
                                       'value': '90397226-1512386903-%7C1512614102',
                                       'domain': 'qyxy.baic.gov.cn',
                                       'path': '/'},
                                      {'name': 'UM_distinctid',
                                       'value': '16021982ad726-0ab7a6b0411555-173f6d56-13c680-16021982ada3c9',
                                       'domain': '.baic.gov.cn',
                                       'path': '/'}]
        #
        return [FormRequest("http://qyxy.baic.gov.cn/es/esAction!entlist.dhtml?currentTimeMillis=1512616476113&credit_ticket=21FE99B0348F1E85450AD1FFC3761903&check_code=4",formdata={
            'queryStr': "邻里家（北京）商贸有限公司",
            'module': '',
            'idFlag': 'qyxy',
        }, cookies=TestSpider.current_cookies, callback=self.after_login)]

    # def init2(self, response):
    #     return Request(url="http://qyxy.baic.gov.cn/simple/dealSimpleAction!transport_ww.dhtml",
    #                    cookies=TestSpider.current_cookies,
    #                    callback=self.after_login)

    # def init(self, response):
    #     TestSpider.current = str(response.xpath('//input[@id="currentTimeMillis"]/@value').extract_first())
    #
    #     TestSpider.image_url = str(response.xpath('//img[@id="MzImgExpPwd"]/@src').extract_first())
    #
    #     # return Request(url="http://qyxy.baic.gov.cn/CheckCodeYunSuan?currentTimeMillis=" + TestSpider.current + "",
    #     #                callback=self.get_image)
    #
    #     # captchapicfile = "/Users/xuxiaoshuo/work/python/codespider/codespider/captcha.png"
    #     # urllib.request.urlretrieve(
    #     #     "http://qyxy.baic.gov.cn" + TestSpider.image_url,
    #     #     filename=captchapicfile)
    #
    #     # Image.open(response.body).show()
    #
    #     captcha = input("输入验证码current"+TestSpider.current+"\n")
    #
    #     return Request(
    #         "http://qyxy.baic.gov.cn/login/loginAction!checkCode.dhtml?check_code=" + captcha + "&currentTimeMillis=" + TestSpider.current + "&random=75612",
    #         cookies=TestSpider.current_cookies,
    #         callback=self.after_login)

    # def get_image(self, response):
    #     captchapicfile = "/Users/xuxiaoshuo/work/python/codespider/codespider/captcha.png"
    #     urllib.request.urlretrieve(
    #         "http://qyxy.baic.gov.cn"+TestSpider.image_url,
    #         filename=captchapicfile)
    #
    #     # Image.open(response.body).show()
    #
    #     captcha = input("输入验证码\n")
    #
        # return [FormRequest("http://qyxy.baic.gov.cn/login/loginAction!checkCode.dhtml", formdata={
        #     'check_code': captcha,
        #     'currentTimeMillis': str(int(time.time())),
        #     'random': '74065',
        # }, callback=self.after_login)]

    # def login(self, response):
    #     print("body002")
    #
    #     # 登录动作
    #     return [FormRequest("http://qyxy.baic.gov.cn/login/loginAction!checkCode.dhtml", formdata={
    #         'check_code': selzf.get_image(response),
    #         'currentTimeMillis': str(int(time.time())),
    #         'random': '74065',
    #     }, callback=self.after_login)]
    #     #

    def after_login(self, response):
        print("bodyend")

        self.log('body %s' % response.body_as_unicode())
        # 现在已经收到登录请求的响应了
        # if json.loads(response.body)['msg'].encode('utf8') == "登陆成功":
        #     yield self.make_requests_from_url('http://www.zhihu.com/people/droiz')
        # else:
        #     print
        #     "验证码错误"
