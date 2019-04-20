# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdCommoditySearchItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    commodity_id = scrapy.Field()#商品id
    commodity_url = scrapy.Field()#商品详情页url
    commodity_title = scrapy.Field()#商品标题
    shop_name = scrapy.Field()#店铺名称
    commodity_price = scrapy.Field()#商品价格
    commodity_brand = scrapy.Field()#品牌
    commodity_model = scrapy.Field()#商品型号
    comment_num = scrapy.Field()
    comment_good_num = scrapy.Field()#好评
    comment_general_num = scrapy.Field()#中评
    comment_poor_num = scrapy.Field()#差评

