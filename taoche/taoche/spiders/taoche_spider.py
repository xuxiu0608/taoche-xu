# xuxiu
# xuxiu2
import re
import socket
import scrapy
from .city import CAR_CODE_LIST,CITY_CODE
from ..my_settings import CUSTOM_SETTING
from scrapy_redis.spiders import RedisSpider
class TaocheSpiderSpider(RedisSpider):
    name = 'taoche_spider'
    # allowed_domains = ['www']
    custom_settings = CUSTOM_SETTING
    redis_key = 'taoche:start_urls'
    myaddr = socket.gethostbyname(socket.gethostname())
    start_urls = []
    for city in CITY_CODE:
        for car in CAR_CODE_LIST:
            base_url = f'https://{city}.taoche.com/{car}/?page=1'
            start_urls.append(base_url)

    def parse(self, response):
        li_list = response.xpath('//ul[@class="gongge_ul"]/li')

        if li_list:
            for li in li_list:
                car_name = li.xpath('.//div[@class="gongge_main"]//span/text()').extract_first()
                car_date = li.xpath('.//div[@class="gongge_main"]//p/i[1]/text()').extract_first()
                car_licheng = li.xpath('.//div[@class="gongge_main"]//p/i[2]/text()').extract_first()
                car_city = li.xpath('.//div[@class="gongge_main"]//p/i[3]/text()').extract_first()
                car_price = li.xpath('.//div[@class="price"]/i/text()').extract_first()
                detail_url = li.xpath('//div[@class="gongge_main"]/a/@href').extract_first()
                item = {}
                item['car_name'] = car_name
                item['car_date'] = car_date
                item['car_licheng'] = car_licheng
                item['car_city'] = car_city.strip()
                item['car_price'] = car_price
                item['detail_url'] = detail_url
                item['ip'] = self.myaddr
                # print(item)
                yield item

            #下一页
            current_page_num = int(re.search(r'\?page=(\d+)',response.url).group(1))
            next_url = re.sub(r'\?page=\d+$',f'?page={current_page_num+1}',response.url)
            # print(next_url)
            yield scrapy.Request(url=next_url,callback=self.parse,encoding='utf-8')

