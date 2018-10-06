# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from amazon.items import AmazonItem


class AmazonspiderSpider(CrawlSpider):
    name = 'amazonspider'
    allowed_domains = ['amazon.cn']
    start_urls = ['https://www.amazon.cn/s/ref=sv_cps_0?ie=UTF8&node=665002051&page=1']

    # 获取单个商品的跳转URL
    detail_le = LinkExtractor(restrict_xpaths=('//div[@class="a-row a-spacing-none"]/a'))

    # 获取列表页下一页URL
    next_le = LinkExtractor(restrict_xpaths=('//a[@id="pagnNextLink"]'))

    # 定义Rule
    rules = (
        Rule(next_le, follow=True),
        Rule(detail_le, follow=False, callback='parse_detail')
    )

    def parse_detail(self, response):
        item = AmazonItem()

        # 获取手机名称
        name = response.xpath('//span[@id="productTitle"]/text()').extract_first().strip()

        # 获取价格
        price = response.xpath('//span[@id="priceblock_ourprice"]/text()').extract_first()

        # 提交数据
        if name is not None and price is not None:
            item["name"] = name
            item["price"] = price
            yield item
