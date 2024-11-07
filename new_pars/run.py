import asyncio
from asyncio import TaskGroup
import json
import time
from abc import ABC, abstractmethod
from .src.generators import CatalogDataGenerator
from .src.generators import CatalogListGenerator
from .src.generators import PricePoolGenerator
from .src.utils import QueryItemsInfo
from .src.Response import PageResponse, CatalogResponse
from .src.Parser import ParserCatalog
from httpx import AsyncClient, Response
from .src.Logger import ResponseLogger
from .src.Postgres import Postgres
from .src.models import category_table, items_table


class BaseClient(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def init_client(self):
        pass


class CatalogClient(BaseClient):

    def __init__(self,
                 log):
        self.log = log

    async def init_client(self):
        async with AsyncClient(http2=True) as client:
            catalog: Response = CatalogResponse(client=client)
            response_catalog_raw = await catalog.get_response()
            catalog_data_json = response_catalog_raw.json()
            parser_catalog = ParserCatalog()
            await parser_catalog.get_cat_info(data=catalog_data_json)
        return parser_catalog.cat_data


class PageClient(BaseClient):

    def __init__(self,
                 log,
                 catalog_list,
                 price_start,
                 price_end,
                 price_step):
        self.catalog_list = catalog_list
        self.price_start = price_start
        self.price_end = price_end
        self.price_step = price_step
        self.data = {}
        self.task_list = {}
        self.items_info = {}
        self.log = log

    async def init_client(self):
        list_catalog = CatalogListGenerator()
        catalog_data = CatalogDataGenerator()
        price = PricePoolGenerator(price_start=self.price_start,
                                   price_end=self.price_end,
                                   price_step=self.price_step)
        async with AsyncClient(http2=True) as client:
            async for category in (list_catalog.
                                   generator(
                                             catalog_list=self.catalog_list)):
                self.log.info(category)
                async with TaskGroup() as tg:
                    async for price_fin in price.generator():
                        query = QueryItemsInfo(shard=category.get('shard'),
                                               id=category.get('id_cat'),
                                               price_filter_min=price_fin,
                                               price_filter_max=price_fin
                                               + self.price_step)
                        # self.log.info(query.query)
                        page = PageResponse(url=query.query,
                                            client=client)
                        self.data[price_fin] = (tg.
                                                create_task
                                                (page.pages_response_old())
                                                )
            return self.data


async def run():
    pg_client = Postgres()
    await pg_client.pg_client()
    logger = ResponseLogger()
    log = logger.log
    start_time = time.time()
    catalog = CatalogClient(log=log)
    catalog_list = await catalog.init_client()
    log.info(catalog_list)
    query_cat = await pg_client.query_bd_cat(data=catalog_list,
                                             table=category_table)
    await pg_client.insert_to_bd(query=query_cat)
    page_data = PageClient(log=log,
                           catalog_list=catalog_list[1:2],
                           price_start=0,
                           price_end=350,
                           price_step=350)
    page_data_res = await page_data.init_client()
    for key, value in page_data_res.items():
        res = await value
        if res is not None:
            for item in res:
                query_items = await pg_client.query_bd_cat(data=(item.get('id'),
                                                                 item.get('brand'),
                                                                 item.get('name')
                                                                 ),
                                                           table=items_table)
                await pg_client.insert_to_bd(query=query_items)
                # with open('new_pars/test.json', 'a') as file:
                #     json.dump(item, file, ensure_ascii=False, indent=4)
                log.info(f"|||||||{res.index(item)}||||||||")
                # for k, v in item.items():
                #     log.info(f"|||||||{k}||||||||")
                # for i in item:
                #     log.info(f"|||||||{item.index(i)}||||||||")
            # for k in res:
            #     log.info(f"|||||||{k}||||||||")
        # for k in res:
        #     for item in k:
        #         for a in item:
        #             log.info(f"|||||||{type(a)}||||||||")
        # res = await page_data_res[key]
        # with open('new_pars/test.json', 'a') as file:
        #     json.dump(res, file, ensure_ascii=False, indent=4)
        # log.info(f'----------------------{key}----------------------')
        # log.info(f'\n{await page_data_res[key]}\n')
    end_time = time.time()
    log.info(end_time - start_time)


def main():
    asyncio.run(run())


if __name__ == '__main__':
    main()
