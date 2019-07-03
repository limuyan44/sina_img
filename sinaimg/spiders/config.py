# -*- coding:utf-8 -*-
# author:blog.zycat.top
# datetime:03/07/2019 08:17
# software: PyCharm


class Config():
    _cookie = "xxx"
    # 文件根目录
    _img_store = 'D:\爬虫图片'
    # 图片文件夹名称
    _folder_name = "美腿"
    # 电脑端评论页地址
    _comment_url = "https://weibo.com/2926793073/HB35eecAH?filter=hot&root_comment_id=0&type=comment"

    def get_cookie(self):
        return self._cookie

    def get_img_store(self):
        return self._img_store

    def get_folder_name(self):
        return self._folder_name

    def get_comment_url(self):
        return self._comment_url
