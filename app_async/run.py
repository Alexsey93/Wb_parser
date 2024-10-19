import asyncio
from app_async.modules.Client import Client
import json


async def run_script(url):
    """Создает объект класса Client,
       получает ответ от метода класса create_task
    Принимает:
        url (str): url адрес ресурса
    """
    client = Client(url=url,
                    semaphore=10)
    response = await client.create_task()
    data = json.loads(response.text)
    print(data)


def main():
    url = ('https://static-basket-01.' +
           'wbbasket.ru/vol0/data/main-menu-ru-ru-v3.json'
           )
    asyncio.run(run_script(url=url))


if __name__ == '__main__':
    main()
