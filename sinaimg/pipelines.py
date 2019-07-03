# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline


class SinaImgPipeline(object):
    def process_item(self, item, spider):
        return item


class ImagesrenamePipeline(ImagesPipeline):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "DNT": "1",
        "Host": "wx2.sinaimg.cn",
        "If-Modified-Since": "Mon, 08 Jul 2013 18:06:40 GMT",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
    }

    def get_media_requests(self, item, info):
        print("========================================")
        print(item['image_urls'])
        print("========================================")
        for image_url in item['image_urls']:
            # 阻止服务器返回304
            yield Request(image_url + '?v=3', meta={'item': item})

    def file_path(self, request, response=None, info=None):
        folder = request.meta['item']['folder_name']
        return super().file_path(request, response, info).replace("full", folder)
