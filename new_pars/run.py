import asyncio
import json
from tqdm import tqdm
from asyncio import TaskGroup, Semaphore
from .src.utils import QueryItemsInfo
from .src.Response import PageResponse, CatResponse
from .src.Parser import ParserCatalog
from fake_useragent import UserAgent
from httpx import AsyncClient
from httpx import Timeout, Limits, Response
from .src.Logger import ResponseLogger
import time
import tqdm.asyncio


async def gen_cat(data_cat):
    for item in data_cat:
        yield item


async def gen_item_cat(item_cat):
    for key in item_cat:
        yield key


async def gen_price(price_start,
                    price_end,
                    price_step):
    for price in range(price_start,
                       price_end,
                       price_step):
        yield price


async def run():
    logger = ResponseLogger()
    logger.create_logger()
    log = logger.log
    start_time = time.time()
    timeout = Timeout(10,
                      read=10,
                      connect=10)
    limits = Limits(max_keepalive_connections=None,
                    max_connections=None)
    agent = UserAgent().random
    url = ('https://static-basket-01.wbbasket.ru/vol0/data/main-menu-ru-ru-v3.json')
    async with AsyncClient(http2=True,
                           limits=limits) as client:
        page = CatResponse(url=url,
                           timeout=timeout,
                           agent=agent,
                           client=client)
        catalog_data_raw: Response = await page.get_response()
        # print(cat_data.json())
        catalog_data_json = catalog_data_raw.json()
        parser_catalog_data = ParserCatalog()
        await parser_catalog_data.get_cat_info(data=catalog_data_json)
        catalog_data = parser_catalog_data.cat_data
        data = {}
        cat_info = {}
        async for category in gen_cat(catalog_data[:1]):
            async for key in gen_item_cat(category):
                async with TaskGroup() as tg:
                    async for price in gen_price(0,
                                                 100000,
                                                 500):
                        query = QueryItemsInfo(shard=category.get(key)[0],
                                               id=category.get(key)[1],
                                               price_filter_min=price,
                                               price_filter_max=price + 500)
                        page = PageResponse(url=query.query,
                                            timeout=timeout,
                                            agent=agent,
                                            client=client)
                        log.info(query.query)
                        data[price] = tg.create_task(page.pages_response())
                cat_info[key] = data
                log.info([type(res) for res in
                          [items for items in
                           [value for key, value in
                            cat_info.items()]
                           ]
                          ])
                    # with open('test.json', 'a') as file:
                    #     json.dump(res, file, ensure_ascii=False, indent=4)
        # res = await value
        # if res:
        #     with open('test.json', 'a') as file:
        #         json.dump(res, file, ensure_ascii=False, indent=4)
    end_time = time.time()
    log.info(end_time - start_time)
        # res = await data[key]
        # print(res)
        # for key, value in data.items():
        #     print(await value)


def main():
    asyncio.run(run())


if __name__ == '__main__':
    main()
