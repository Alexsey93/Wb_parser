from asyncio import TaskGroup
import json
from httpx import Response
from app_async.modules.Client import Client, decorators
import asyncio


class Parser:

    def __init__(self):
        pass

    async def get_catalog_data(self, data=None, list_cat=None):
        dict_cat = {}
        if list_cat is None:
            list_cat = []
        if isinstance(data, list):
            for category in data:
                # print(f'-----\n\n\n{category}\n\n\n-----')
                await self.get_catalog_data(data=category, list_cat=list_cat)
        elif isinstance(data, dict):
            if 'childs' in data:
                # print(f'\n\n\n{data.get('childs')}\n\n\n')
                await self.get_catalog_data(data=data.get('childs'), list_cat=list_cat)
            else:
                if data.get('shard'):
                    if data.get('shard') != 'blackhole':
                        dict_cat[data.get('name')] = [data.get('shard'),
                                                      data.get('id')]
                        list_cat.append(dict_cat)
        return list_cat
            # for key, value in data.items():
                # print(key)
                # print('\n----------------------------------------------\n')
                # print(value)
    # def get_catalog_data(self, data=None, list_cat=None, count=0):
    #     dict_cat = {}
    #     if list_cat is None:
    #         list_cat = []
    #     if isinstance(data, list):
    #         for category in data:
    #             self.get_catalog_data(data=category, list_cat=list_cat)
    #     else:
    #         for key, value in data.items():
    #             if key == 'childs':
    #                 # print(data['name'], data['shard'], end="\n\n\n")
    #                 self.get_catalog_data(value, list_cat=list_cat, count=count)
    #             else:
    #                 if (data.get('shard') and data.get('shard') != 'blackhole' and data.get('shard') != ''):
    #                     dict_cat[data.get('name')] = [data.get('id'),
    #                                                   data.get('shard')]
    #                     list_cat.append(dict_cat)
    #                     count = count + 1
    #     return list_cat
    
    # async def gen_page(max_page=50):
    #     for page in range(max_page)
    #         yield page
            
    
    @decorators.validator_json
    @decorators.retry(max_retry=10)
    @decorators.get_response
    async def parser_page(self,
                          page=1,
                          id_cat=None,
                          shard=None,) -> str:
        # print(shard, id_cat, page)
        url = f'https://catalog.wb.ru/catalog/{shard}/v2/catalog?ab_testing=false&appType=1&cat={id_cat}&curr=rub&dest=-5817685&sort=popular&spp=30&page={page}'
        # print(url)
        return url

    # async def parser_cat(self,
    #                      client=None,
    #                      tg: TaskGroup = None,
    #                      id_cat=None,
    #                      max_page=50,
    #                      shard=None,
    #                      name_cat=None):
    #     # data_cat = {}
    #     async for page in self.gen_page_num(max_page):
    #         print(page, id_cat, name_cat)
    #         tg.create_task(self.parser_page(client=client,
    #                                         page=page,
    #                                         id_cat=id_cat,
    #                                         shard=shard,
    #                                         name_cat=name_cat))
