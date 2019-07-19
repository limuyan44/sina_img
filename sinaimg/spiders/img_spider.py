# -*- coding:utf-8 -*-
# author:blog.zycat.top
# datetime:03/07/2019 03:11
# software: PyCharm
import json
import os
import re
import requests
import scrapy
import time
import random
from lxml import etree

from sinaimg.items import SinaImgItem
from sinaimg.spiders.config import Config


class ImgSpider(scrapy.Spider):
    config = Config()
    name = 'ImgSpider'
    headers = {
        "Accept": "*/*"
        , "Accept-Encoding": "gzip, deflate, br"
        , "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
        , "Connection": "keep-alive"
        , "Content-Type": "application/x-www-form-urlencoded"
        , "DNT": "1"
        , "Host": "weibo.com"
        , "Referer": "https://weibo.com/1749127163/HBvsZliX7?filter=hot&root_comment_id=4389391167963123&type=comment"
        ,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
        , "X-Requested-With": "XMLHttpRequest"
        ,
        "Cookie": config.get_cookie()
    }
    custom_settings = {
        # 图片保存地址
        "IMAGES_STORE": config.get_img_store()
    }
    base_url = "https://weibo.com/aj/v6/comment/big?ajwvr=6&id={}&page={}"

    # 文件夹名称
    folder_name = config.get_folder_name()
    # 评论地址
    comment_url = config.get_comment_url()

    def start_requests(self):
        self.write_url(self.custom_settings.get("IMAGES_STORE") + "\\" + self.folder_name, self.comment_url)
        id = self.get_comment_url()
        if not id:
            print("===============请更新cookie重新登录============")
            return None
        url = self.base_url.format(id, '1')
        r = requests.get(url=url, headers=self.headers)
        if r.content:
            print(r.content)
            html = json.loads(r.content.decode('utf-8'))
            totalpage = html['data']['page']['totalpage']
            urls = []
            for i in range(1, totalpage + 1):
                page_url = self.base_url.format(id, str(i))
                time.sleep(random.uniform(1, 2))
                response = requests.get(url=page_url, headers=self.headers)
                html = json.loads(response.content.decode('utf-8'))
                html_page = html['data']['html']
                element = etree.HTML(html_page)
                img_urls = element.xpath('//*[@class="list_box"]//li[@class="WB_pic S_bg2 bigcursor"]/img/@src')
                item = SinaImgItem()
                img_urls = ['http://' + url.replace('/thumb180/', '/large/')[2:] for url in img_urls]
                urls.extend(img_urls)
            item['image_urls'] = urls
            item['folder_name'] = self.folder_name
            yield scrapy.Request(url='http://www.baidu.com', callback=self.parse, meta={'item': item})

        else:
            print("未获取到评论")
            print(r.status_code)
            print(r.content)
            return None

    def parse(self, response):
        item = response.meta['item']
        yield item

    def get_comment_url(self):
        r = requests.get(url=self.comment_url, headers=self.headers)
        if r.status_code != 200:
            print(r.content)
            return None
        s = re.findall(r"act=(.+?)\\\"", r.content.decode('utf-8'))
        if not s:
            return None
        return s[0]

    def write_url(self, path, url):
        '''
        保存一个评论链接地址
        :return:
        '''
        path = path
        if not os.path.exists(path):
            os.makedirs(path)
        with open(path + "\\图片原微博地址.txt", "wb") as f:
            f.write(url.encode())


def run():
    from scrapy import cmdline

    args = "scrapy crawl ImgSpider".split()
    cmdline.execute(args)


if __name__ == '__main__':
    run()
