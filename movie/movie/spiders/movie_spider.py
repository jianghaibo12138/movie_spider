# coding=utf8

import os
import sys

from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http.request import Request
from movie.items import MovieItem

class MovieSpider(Spider):
    name = "movie"
    allowed_domains = ["http://www.666hdhd.com/"]
    start_urls = [
        "http://www.666hdhd.com/",
    ]
    dir_path = "./urls/"
    file_name = ["记录.txt", "剧情.txt", "喜剧.txt", "科幻.txt", "战争.txt", "动作.txt", "爱情.txt", "恐怖.txt", "传记.txt", "动画.txt"]
    movie_handle = {
        u"记录" : dir_path + file_name[0],
        u"纪录" : dir_path + file_name[0],
        u"剧情" : dir_path + file_name[1],
        u"喜剧" : dir_path + file_name[2],
        u"科幻" : dir_path + file_name[3],
        u"战争" : dir_path + file_name[4],
        u"动作" : dir_path + file_name[5],
        u"爱情" : dir_path + file_name[6],
        u"恐怖" : dir_path + file_name[7],
        u"传记" : dir_path + file_name[8],
        u"动画" : dir_path + file_name[9],
        }


    def parse_next(self, response):
        sel = Selector(response)
        url_bs = self.parse_movie(sel)
        for url in url_bs:
            yield Request(url, callback = self.parse_download, dont_filter = True)


    def parse_item(self, response):
        sel = Selector(response)
        urls = sel.xpath("//div/a/@href").extract()
        for url in urls:
            if not "list" in url or "_____1" in url:
                continue
            url = self.start_urls[0] + url[1:]
            yield Request(url, callback = self.parse_next, dont_filter = True)

        url_bs = self.parse_movie(sel)
        for url in url_bs:
            yield Request(url, callback = self.parse_download, dont_filter = True)

    def parse(self, response):
        if not os.path.exists(self.dir_path):
            os.makedirs(self.dir_path)
        for file_name in self.file_name:
            file_path = self.dir_path + file_name
            if os.path.exists(file_path):
                os.remove(file_path)

        sel = Selector(response)

        urls = sel.xpath("//div/ul/li/a/@href").extract()

        url_bs = []
        for url in urls:
            if len(url) < 5 or "help" in url:
                continue
            url = self.start_urls[0] + url[1:]
            if "movielist" in url:
                yield Request(url, callback = self.parse_item, dont_filter=True)


    def parse_movie(self, sel):
        urls = sel.xpath("//div/ul/li/a/@href").extract()
        url_bs = []
        for url in urls:
            if len(url) < 5 or "help" in url:
                continue
            url = self.start_urls[0] + url[1:]
            if "movielist" in url:
                continue
            else:
                url_bs.append(url)
        return url_bs


    def parse_download(self, response):
        sel = Selector(response)
        urls = sel.xpath("//div/li/a/@href").extract()
        names = []
        for url in urls:
            name = url.split("/")[-1]
            name = name.split(".")[0]
            names.append(name)
        self.save_movie_list(urls, names)


    def save_movie_list(self, urls, names):
        # 解决unicode字符串和str串拼接问题
        reload(sys)
        sys.setdefaultencoding("utf8")
        # fobj = open(file_path, "awb+")
        for url in urls:
            if "http" in url and "pan" not in url:
                ul = url.split("/")
                fobj = open(self.movie_handle[ul[3][0:2]], "awb+")
                # if ul[3][0:2] not in self.movie_type:
                    # self.movie_type.append(ul[3][0:2])
                f_str = url + "\n"
                fobj.write(f_str)
                fobj.close()
        # print self.movie_type
