import asyncio
from asyncio import TaskGroup
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
                async for key in catalog_data.generator(catalog_data=category):
                    async with TaskGroup() as tg:
                        async for price_fin in price.generator():
                            query = QueryItemsInfo(shard=category.get(key)[0],
                                                   id=category.get(key)[1],
                                                   price_filter_min=price_fin,
                                                   price_filter_max=price_fin
                                                   + 500)
                            self.log.info(query.query)
                            page = PageResponse(url=query.query,
                                                client=client)
                            self.data[price_fin] = (tg.
                                                    create_task
                                                    (page.pages_response())
                                                    )
            return self.data


async def run():
    logger = ResponseLogger()
    log = logger.log
    start_time = time.time()
    catalog = CatalogClient(log=log)
    catalog_list = await catalog.init_client()
    log.info(catalog_list)
    page_data = PageClient(log=log,
                           catalog_list=catalog_list,
                           price_start=0,
                           price_end=100000,
                           price_step=500)
    page_data_res = await page_data.init_client()
    print(page_data_res)
    end_time = time.time()
    log.info(end_time - start_time)


def main():
    asyncio.run(run())


if __name__ == '__main__':
    main()
