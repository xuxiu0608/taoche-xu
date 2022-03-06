
from .city import CAR_CODE_LIST,CITY_CODE
import redis
#1.新建redis链接
r= redis.Redis()

for city in CITY_CODE:
    for car in CAR_CODE_LIST:
        base_url = f'https://{city}.taoche.com/{car}/?page=1'
        # start_urls.append(base_url)
        r.lpush('taoche:start_urls',base_url)