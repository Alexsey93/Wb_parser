import httpx
import json
from httpx import AsyncClient, Response
import asyncio
from asyncio import Semaphore
from fake_useragent import UserAgent


class decorators():

    def retry(max_retry=None):
        def inner(func):
            async def wrapper(self, *args, **kwargs):
                retry = max_retry
                while retry:
                    try:
                        await asyncio.sleep(0.1)
                        response: Response = await func(self, *args, **kwargs)
                        # print(response.status_code)
                        if response.status_code != 200:
                            raise ConnectionError('ошибка парсинга')
                    except Exception as e:
                        retry = retry - 1
                        print(retry)
                        if retry == 0:
                            return e
                    else:
                        return response
            return wrapper
        return inner

    def get_response(func):
        async def wrapper(self, *args, **kwargs):
            agent = UserAgent()
            __accept_language = 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'
            headers = {
                            'User-Agent': agent.random,
                            'Accept': '*/*',
                            'Accept-Language': __accept_language,
                            # 'Accept-Encoding': 'gzip, deflate, br, zstd',
                            'Access-Control-Request-Method': 'GET',
                            'Access-Control-Request-Headers': 'x-captcha-id',
                            'Referer': 'https://www.wildberries.ru/',
                            'Origin': 'https://www.wildberries.ru',
                            'Connection': 'keep-alive',
                            'Sec-Fetch-Dest': 'empty',
                            'Sec-Fetch-Mode': 'cors',
                            'Sec-Fetch-Site': 'cross-site',
                            'Priority': 'u=4',
                            'Pragma': 'no-cache',
                            'Cache-Control': 'no-cache',
                            # Requests doesn't support trailers
                            # 'TE': 'trailers',
                        }
            timeout = httpx.Timeout(10,
                                    read=10,
                                    connect=10)
            limits = httpx.Limits(max_keepalive_connections=100,
                                  max_connections=100)
            url = await func(self, *args, **kwargs)
            async with AsyncClient(limits=limits) as session:
                semaphore = Semaphore(51)
                async with semaphore:
                    response = await session.get(url=url,
                                                 headers=headers,
                                                 timeout=timeout)
                    # print(response)
                    # print(url)
            return response
        return wrapper

    def validator_json(func):
        async def wrapper(*args, **kwargs):
            try:
                response: Response = await func(*args, **kwargs)
                # print(response)
                if response:
                    return response.json()
                else:
                    print('нет данных')
                    raise ConnectionError('нет данных')
            except Exception as e:
                # print(e)
                return e
            else:
                print(response, '2-\n')
                return response
        return wrapper


class Client:

    def __init__(self,
                 semaphore: int = None,
                 ) -> None:
        self.__accept_language = 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'
        self.agent = UserAgent()
        self.semaphore = semaphore
        self.headers = {
                        'User-Agent': self.agent.random,
                        'Accept': '*/*',
                        'Accept-Language': self.__accept_language,
                        # 'Accept-Encoding': 'gzip, deflate, br, zstd',
                        'Access-Control-Request-Method': 'GET',
                        'Access-Control-Request-Headers': 'x-captcha-id',
                        'Referer': 'https://www.wildberries.ru/',
                        'Origin': 'https://www.wildberries.ru',
                        'Connection': 'keep-alive',
                        'Sec-Fetch-Dest': 'empty',
                        'Sec-Fetch-Mode': 'cors',
                        'Sec-Fetch-Site': 'cross-site',
                        'Priority': 'u=4',
                        'Pragma': 'no-cache',
                        'Cache-Control': 'no-cache',
                        # Requests doesn't support trailers
                        # 'TE': 'trailers',
                    }
    @decorators.validator_json
    @decorators.retry(max_retry=10)
    @decorators.get_response
    async def page_data_cat(self) -> str:
        url = ('https://static-basket-01.' +
               'wbbasket.ru/vol0/data/main-menu-ru-ru-v3.json')
        return url

    # @decorators.parser_cat_to_json
    # @decorators.retry(max_retry=10)
    # async def get_response(self,
    #                        url=None,
    #                        ) -> httpx.Response:
    #     print(url)
    #     timeout = httpx.Timeout(10,
    #                             read=100,
    #                             connect=10)
    #     limits = httpx.Limits(max_keepalive_connections=100,
    #                           max_connections=100)
    #     async with AsyncClient(limits=limits) as session:
    #         semaphore = Semaphore(self.semaphore)
    #         async with semaphore:
    #             try:
    #                 response = await session.get(url=url,
    #                                              headers=self.headers,
    #                                              timeout=timeout)
    #             except Exception as e:
    #                 return e
    #             else:
    #                 return response


                    # print(respon se.text)
                #     if (response.status_code == 200 and response.text is not None):
                #         print(f'[+] категория - {name_cat} страница - {page} - попытка {retry}')
                #         print(self.url)
                #     else:
                #         print(f'[-] категория - {name_cat} страница - {page} - попытка {retry}')
                #         print(f'Ошибка обработки - {response.status_code} или json пуст')
                #         raise ConnectionError('возникла ошибка')
                # except Exception as e:
                #     if retry:
                #         print(f'[INFO] retry={retry} => {self.url}:{page}') 
                #         print('-- ресурс недоступен или не существует ')
                #         return await self.get_response(url=url,
                #                                        timeout=timeout,
                #                                        page=page,
                #                                        name_cat=name_cat,
                #                                        retry=(retry-1))
                #     else:
                #         print(e)
                # else:
                #     return response
