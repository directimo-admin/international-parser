
# Scrapy settings for condoparser project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import os

BOT_NAME = 'condoparser'

SPIDER_MODULES = ['condoparser.spiders']
NEWSPIDER_MODULE = 'condoparser.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True
REDIRECT_ENABLED = False

# The download delay setting will honor only one of:
DOWNLOAD_DELAY = 3

COOKIES_ENABLED = False

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'condoparser.pipelines.CondoparserPipeline': 300,
}

# enable the middleware
DOWNLOADER_MIDDLEWARES = {
    'scrapy_zyte_smartproxy.ZyteSmartProxyMiddleware': 610}
# enable Zyte Proxy
ZYTE_SMARTPROXY_ENABLED = True
# the APIkey you get with your subscription
ZYTE_SMARTPROXY_APIKEY = 'YOUR_KEY'
AUTOTHROTTLE_ENABLED = False
CONCURRENT_REQUESTS = 32
CONCURRENT_REQUESTS_PER_DOMAIN = 32
DOWNLOAD_TIMEOUT = 600
ZYTE_SMARTPROXY_PRESERVE_DELAY = True
