#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
author:Herish
datetime:2019/4/18 19:51
software: PyCharm
description: 
'''
import scrapy
from scrapy import Request
from jd_commodity_search.items import JdCommoditySearchItem
import json

# 爬取的商品页数
PAGES = 2
# 商品列表的初始页
START_PAGE = 1


class JdCommoditySpider(scrapy.Spider):
    name = 'jd_commodity_search'

    allowed_domains = ['jd.com']
    # 爬取的商品名称
    keyWords = '手机'
    # 商品列表页的请求地址
    start_urls = [
        'https://search.jd.com/Search?keyword={0}&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&cid2=653&cid3=655&page={1}&click=0']
    # 商品列表页 异步加载得到的剩余的30个商品的请求地址
    later_thirty_url = 'https://search.jd.com/s_new.php?keyword={0}&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&cid2=653&cid3=655&page={1}&scrolling=y&tpl=3_M&show_items={2}'
    # 商品评论js页面的请求地址
    comment_url = 'https://club.jd.com/comment/productCommentSummaries.action?referenceIds={}'
    # 商品详情请求地址
    commodity_url = 'https://item.jd.com/{0}.html'

    def start_requests(self):
        for each in range(START_PAGE, PAGES):
            # 请求商品列表页，获取的商品列表页只包含前30个商品（每页共有60个）
            yield Request(url=self.start_urls[0].format(self.keyWords, each), callback=self.parse)

    def parse(self, response):
        page_url = response.url
        #获取当前页面数
        page = int(''.join(page_url.split('&')[-2][5:]))

        # commodity_ids用于获取商品id
        commodity_ids = []
        commodity_items = response.css('.gl-item')
        for commodity in commodity_items:
            item = JdCommoditySearchItem()
            # 商品价格
            item['commodity_price'] = commodity.css('.p-price > strong > i::text').extract_first()
            if item['commodity_price'] == None:  # 当提取商品价格返回为None时，说明该商品暂时无货
                continue
            else:
                item['commodity_price'] = float(item['commodity_price'])
            # 商品详情页请求地址
            item['commodity_url'] = commodity.css('.p-img a::attr(href)').extract_first()
            if 'http' not in item['commodity_url']:
                item['commodity_url'] = 'https:' + item['commodity_url']
            # 商品id
            item['commodity_id'] = commodity.css('.gl-item::attr(data-sku)').extract_first()
            commodity_ids.append(item['commodity_id'])

            # 评论页地址
            comment_url = self.comment_url.format(item['commodity_id'])
            yield Request(url=comment_url, callback=self.parseComment, meta={'item': item})

        page += 1
        # 已经展示出来的30个商品
        show_items_ids = ','.join(commodity_ids)
        yield Request(url=self.later_thirty_url.format(self.keyWords, page, show_items_ids), callback=self.parseNext,
                      headers={'Referer': page_url},meta={'commodity_ids':commodity_ids})

    def parseNext(self, response):
        '''
        处理方法和parse函数基本无差别，用于加载后30个商品信息
        :param response:
        :return:
        '''
        old_ids = response.meta['commodity_ids']
        commodity_items = response.css('.gl-item')

        for commodity in commodity_items:
            item = JdCommoditySearchItem()
            # 商品价格
            item['commodity_price'] = commodity.css('.p-price > strong > i::text').extract_first()
            if item['commodity_price'] == None:  # 当提取商品价格返回为None时，说明该商品暂时无货
                continue
            else:
                item['commodity_price'] = float(item['commodity_price'])
            # 商品详情页请求地址
            item['commodity_url'] = commodity.css('.p-img a::attr(href)').extract_first()
            if 'http' not in item['commodity_url']:
                item['commodity_url'] = 'https:' + item['commodity_url']
            # 商品id
            item['commodity_id'] = commodity.css('.gl-item::attr(data-sku)').extract_first()
            # commodity_ids.append(item['commodity_id'])
            # 商品页面加载后30个商品的时候，存在重复的情况，根据商品id区分，重复的id不做详细查询
            if item['commodity_id'] in old_ids:
                continue
            else:
                old_ids.append(item['commodity_id'])

            # 评论页地址
            comment_url = self.comment_url.format(item['commodity_id'])
            yield Request(url=comment_url, callback=self.parseComment,
                          meta={'item': item})

    def parseComment(self, response):
        '''
        主要爬取评论数目
        :param response:
        :return:
        '''
        # 获取评论信息
        item = response.meta['item']
        comment_dict = json.loads(response.text)['CommentsCount'][0]
        # 获取商品总评论数
        item['comment_num'] = comment_dict.get('CommentCount', 0)
        # 商品好评数
        item['comment_good_num'] = comment_dict.get('GoodCount', 0)
        # 商品中评数
        item['comment_general_num'] = comment_dict.get('GeneralCount', 0)
        # 商品差评数
        item['comment_poor_num'] = comment_dict.get('PoorCount', 0)

        yield Request(url=item['commodity_url'], callback=self.parseDetail, meta={'item': item})

    def parseDetail(self, response):
        '''
        商品介绍信息提取
        :param response:
        :return:
        '''
        item = response.meta['item']
        # 商品标题
        item['commodity_title'] = response.css('.sku-name').xpath('string()').extract_first().replace('\n', '').replace(
            '\t', '').strip()
        # 商品品牌
        item['commodity_brand'] = response.css('.head a::text').extract_first()
        if not item['commodity_brand']:
            item['commodity_brand'] = response.css('#parameter-brand a::text').extract_first()

        # 商品型号
        item['commodity_model'] = response.css('.item.ellipsis::text').extract_first()
        # 店铺名称
        item['shop_name'] = response.css('.popbox-inner .mt > h3 > a::text').extract_first()
        if not item['shop_name']:
            item['shop_name'] = response.css('.J-hove-wrap .name > a::text').extract_first()

        yield item
