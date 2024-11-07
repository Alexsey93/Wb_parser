from abc import ABC, abstractmethod
from asyncio import TaskGroup
import asyncio
from httpx import Response
import httpx
from .Logger import ResponseLogger


class BaseRetry(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    async def retry():
        pass


class Retry(BaseRetry):

    def __init__(self,
                 max_retry):
        self.max_retry = max_retry
        logger = ResponseLogger()
        self.log: ResponseLogger = logger.log

    @staticmethod
    def retry(max_retry=None):
        def inner(func) -> Response:
            async def wrapper(self, *args, **kwargs):
                retry = max_retry
                while retry:
                    try:
                        await asyncio.sleep(0.2)
                        response: Response = await func(self, *args, **kwargs)
                        if isinstance(response, httpx.ConnectTimeout):
                            raise ConnectionError('ошибка таймаута')
                        if isinstance(response, httpx.ConnectError):
                            raise ConnectionError('ресурс недоступен')
                    except Exception as e:
                        # print(e)
                        retry = retry - 1
                        self.log.info(f'попытка {retry} из {max_retry}')
                        if retry == 0:
                            return e
                    else:
                        return response
            return wrapper
        return inner
