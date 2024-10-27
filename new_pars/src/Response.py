from abc import ABC, abstractmethod
from httpx import AsyncClient, Response
from httpx import ConnectError
from .Retry import Retry
from .Logger import ResponseLogger





class ResponseBase(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    async def get_response():
        pass


class CatResponse(ResponseBase):

    def __init__(self,
                 url,
                 agent,
                 client,
                 timeout):
        self._url = url
        self.agent = agent
        self.client: AsyncClient = client
        self.timeout = timeout
        self.headers = {
            'User-Agent': self.agent,
            'Accept': '*/*',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            # 'Accept-Encoding': 'gzip, deflate, br, zstd',
            # 'x-captcha-id': 'Catalog 1|1|1730537939|AA==|8cfed877739d45c392ce5c3034d3d144|MeMnwrlKTcCOr9cGS7QYIJTdoIcgWcj6SSAT4OopfNL',
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
        logger = ResponseLogger()
        logger.create_logger()
        self.log = logger.log

    @Retry.retry(max_retry=10)
    async def get_response(self) -> Response:
        try:
            response: Response = await self.client.get(url=self._url,
                                                       headers=self.headers)
            self.log.info(f'\n----{self._url}----')
        except Exception as e:
            return e
        else:
            self.response = response
            return response


class PageResponse(ResponseBase):

    def __init__(self,
                 url,
                 agent,
                 client,
                 timeout):
        self._url = url
        self.agent = agent
        self.client: AsyncClient = client
        self.response = []
        self.timeout = timeout
        self.headers = {
            'User-Agent': self.agent,
            'Accept': '*/*',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            # 'Accept-Encoding': 'gzip, deflate, br, zstd',
            # 'x-captcha-id': 'Catalog 1|1|1730537939|AA==|8cfed877739d45c392ce5c3034d3d144|MeMnwrlKTcCOr9cGS7QYIJTdoIcgWcj6SSAT4OopfNL',
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
        logger = ResponseLogger()
        logger.create_logger()
        self.log = logger.log

    @Retry.retry(max_retry=5)
    async def get_response(self,
                           page) -> Response:
        try:
            url = self._url+f'&page={page}'
            # print(self._url+f'&page={page}')
            response: Response = await self.client.get(url=url,
                                                       headers=self.headers)
            if response.status_code == 200:
                return (response,
                        url)
            else:
                raise ConnectError('Ошибка соединения')
            # print(response.status_code)
        except Exception as e:
            return e

    async def pages_response(self, list_response=None, page=None):
        if list_response is None:
            list_response = {}
        if page is None:
            page = 1
        if page == 51:
            return list_response
        response: Response = await self.get_response(page=page)
        if not isinstance(response, ConnectionError):
            self.log.info(f'\n-----    {response}---\n')
            self.log.info(f'\n-----------{page}---{bool(response[0].json().get('data').get('products'))}---{response[1]}-------\n')
            if response:
                if response[0].json().get('data').get('products'):
                    list_response[page] = response[0].json().get('data').get('products')
                    page = page + 1
                    await self.pages_response(list_response=list_response,
                                            page=page)
            else:
                return list_response
        return list_response
