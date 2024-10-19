import httpx
from httpx import AsyncClient
import asyncio
from asyncio import Semaphore
from fake_useragent import UserAgent


class Client():

    def __init__(self,
                 url: str,
                 semaphore: int,
                 ) -> None:
        self.__accept_language = 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'
        self.agent = UserAgent()
        self.url = url
        self.semaphore = semaphore
        self.headers = {
                        'User-Agent': self.agent.random,
                        'Accept': '*/*',
                        'Accept-Language': self.__accept_language,
                        # 'Accept-Encoding': 'gzip, deflate, br, zstd',
                        'Origin': 'https://www.wildberries.ru',
                        'Connection': 'keep-alive',
                        'Referer': 'https://www.wildberries.ru/',
                        'Sec-Fetch-Dest': 'empty',
                        'Sec-Fetch-Mode': 'cors',
                        'Sec-Fetch-Site': 'cross-site',
                        'Priority': 'u=4',
                        'Pragma': 'no-cache',
                        'Cache-Control': 'no-cache',
                        # Requests doesn't support trailers
                        # 'TE': 'trailers',
                    }

    async def get_response(self,
                           session,
                           timeout,
                           retry=10
                           ) -> httpx.Response:
        """Метод для получения сырого ответа от заданного
           ресурса с полученными параметрами сессии
        Принимает:
            session (httpx.AsyncClient): Объект сессии
            timeout (httpx.Timeout): Параметры таймаута сессии
            retry (int, optional): количество попыток подключения

        Возвращает:
            httpx.Response: Ответ ресурса
        """
        semaphore = Semaphore(self.semaphore)
        async with semaphore:
            try:
                await asyncio.sleep(1)
                response = await session.get(url=self.url,
                                             headers=self.headers,
                                             timeout=timeout)
            except Exception as e:
                if retry != 0:
                    print(retry)
                    return await self.get_response(session=session,
                                                   timeout=timeout,
                                                   retry=(retry-1))
                else:
                    print(e)
            else:
                return response

    async def create_task(self) -> httpx.Response:
        """Метод создания сессии и ее передачи
           с установленными параметрами
           в метод get_response
        Возвращает:
            httpx.Response: ответ ресурса
        """
        timeout = httpx.Timeout(10,
                                read=20,
                                connect=10)
        limits = httpx.Limits(max_keepalive_connections=10,
                              max_connections=10)
        async with AsyncClient(limits=limits) as session:
            return await self.get_response(session=session,
                                           timeout=timeout)
