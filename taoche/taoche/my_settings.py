import hashlib
import random

CUSTOM_SETTING = {
    #1.robots协议
    'ROBOTSTXT_OBEY' : False,
    #2.请求头
    'DEFAULT_REQUEST_HEADERS' : {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en',
        # 'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',

    },

    #3.pipelines管道
    'ITEM_PIPELINES' : {
       'taoche.my_settings.MongoPipeline': 300,
       #  'scrapy.pipelines.images.ImagesPipeline':300,
    },
    # 'MONGO_URI':'localhost',
    #保存到mongodb的哪个数据库
    'MONGO_DATABASE':'spider_date',
    #4.下载中间件
    # 'DOWNLOADER_MIDDLEWARES' : {
    #    'sh_company.my_settings.ProxyMiddle': 543,
    # },
    #设置代理方法1
    # 'PROXIES' :[
    #     #     # {'ip_port':'60.166.161.17:4227','user_passwd':None},
    #     # ]

    #scrapy-reids分布式配置
    # scrapy-redis配置
    # 配置scrapy-redis调度器
    'SCHEDULER': "scrapy_redis.scheduler.Scheduler",
    # 配置url去重
    'DUPEFILTER_CLASS': "scrapy_redis.dupefilter.RFPDupeFilter",
    # 配置优先级队列
    'SCHEDULER_QUEUE_CLASS': 'scrapy_redis.queue.PriorityQueue',
    'REDIS_PORT': 6379,

    # 主机
    'REDIS_HOST': 'localhost',
    'MONGO_URI': 'localhost',

    # 从机
    # 'REDIS_HOST': '192.168.33.91',
    # 'MONGO_URI': '192.168.33.91',



}
import pymongo
from itemadapter import ItemAdapter

class MongoPipeline:
    #集合名称配置
    collection_name = 'taoche_car'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        item['item_id'] = get_md5(item['detail_url'])
        self.db[self.collection_name].update_one({'item_id': item['item_id']}, {'$set': item}, upsert=True)
        return item

def get_md5(text):
    return hashlib.md5(text.encode()).hexdigest()

class ProxyMiddle:

    def __init__(self):
        self.USER_AGENGT = [
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
            "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
            "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
            "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
            "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
            "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        ]
        self.PROXY_LIST = [
            '116.149.202.176:4226',
            '113.237.229.89:4250',
            '60.7.2.68:4285',
            '60.166.161.17:4227',
        ]
        pass

    def process_request(self, request, spider):
        #1.如何设置请求头
        ua = random.choice(self.USER_AGENGT)
        request.headers.setdefault('User_Agent',ua)

        #2.设置代理
        # request.meta['proxy'] = 'http://'+random.choice(self.PROXY_LIST)

        # return request
