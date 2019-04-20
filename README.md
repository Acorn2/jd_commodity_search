# jd_commodity_search

京东商品爬虫

根据需求设定搜索内容，爬取指定页数的内容。具体内容包括：

    commodity_id = scrapy.Field()#商品id
    commodity_url = scrapy.Field()#商品详情页url
    commodity_title = scrapy.Field()#商品标题
    shop_name = scrapy.Field()#店铺名称
    commodity_price = scrapy.Field()#商品价格
    commodity_brand = scrapy.Field()#品牌
    commodity_model = scrapy.Field()#商品型号
    comment_num = scrapy.Field()#评论数
    comment_good_num = scrapy.Field()#好评
    comment_general_num = scrapy.Field()#中评
    comment_poor_num = scrapy.Field()#差评
    
对爬取结果进行整理，存入Mongodb中。
