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
    dir_path = "./"


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

        sel = Selector(response)

        urls = sel.xpath("//div/ul/li/a/@href").extract()
        # names = sel.xpath("//div/ul/li/a/span/text()").extract()

        url_bs = []
        for url in urls:
            if len(url) < 5 or "help" in url:
                continue
            url = self.start_urls[0] + url[1:]
            if "movielist" in url:
                yield Request(url, callback = self.parse_item, dont_filter=True)


    def parse_movie(self, sel):
        urls = sel.xpath("//div/ul/li/a/@href").extract()
        # names = sel.xpath("//div/ul/li/a/span/text()").extract()
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
        file_path = self.dir_path + "list.txt"
        reload(sys)
        sys.setdefaultencoding("utf8")
        fobj = open(file_path, "awb+")
        for url in urls:
            if "pan" in url:
                continue
            f_str = url + "\n\n"
            fobj.write(f_str)
        # for x, y in zip(urls, names):
            # if "pan" in x or "ftp" in x:
                # continue
            # f_str = str(y) + "---------" + x.rstrip() + "\n"
            # fobj.write(f_str)
        fobj.close()
