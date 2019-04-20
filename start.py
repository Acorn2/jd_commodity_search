#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
author:Herish
datetime:2019/4/18 19:49
software: PyCharm
description: 
'''
from scrapy import cmdline

cmdline.execute('scrapy crawl jd_commodity_search'.split(' '))