
import asyncio
from app_async.modules.Client import Client
from app_async.modules.Parser import Parser
import json
import time


async def run_script(url):
    """Создает объект класса Client,
       получает ответ от метода класса create_task
    Принимает:
        url (str): url адрес ресурса
    """
    start_time = time.time()
    client = Client(semaphore=200)
    parser = Parser()
    data_cat = await client.page_data_cat()
    list_info_cat = await parser.get_catalog_data(data=data_cat)
    count = 0
    data_items = {}
    for item in list_info_cat[:100]:
        count += 1
        print(item, end='\n_____________________\n')
    print(count)
    print(len(list_info_cat))
    async with asyncio.TaskGroup() as tg:
        for item in list_info_cat[:10]:
            # print(item)
            for key in item:
                page = 1
                while page <= 50:
                    print(key)
                    data_items[key] = tg.create_task(parser.parser_page(page=page,
                                                                        id_cat=item[key][1],
                                                                        shard=item[key][0],
                                                                        ))
                    # res = await data_items[key]
                    page = page + 1
                    # print(res)
    for task in data_items:
        res = await data_items[task]
        print(res)
    # for key, value in data_items.items():
    #     print(key)
    #     await asyncio.sleep(2)
    #     print(value.result())
    # async with asyncio.TaskGroup() as tg:
    #     for key, value in text.items():
    #         items_data[1] = tg.create_task(parser.parser_items(id_cat=value[0],
    #                                                              name_cat=key,
    #                                                              shard=value[1]))
    # for items, values in items_data.items():
    #     res = await values
    #     print(res)
    #     # if res is not None:
        #     print(res, end='\n\n\n')
    end_time = time.time()
    print(end_time - start_time)


def main():
    url = ('https://static-basket-01.' +
           'wbbasket.ru/vol0/data/main-menu-ru-ru-v3.json'
           )
    asyncio.run(run_script(url=url))


if __name__ == '__main__':
    main()
