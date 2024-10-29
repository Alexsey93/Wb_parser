from abc import ABC, abstractmethod


class Query(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    async def prepare_query(self):
        pass


class QueryItemsInfo(Query):

    def __init__(self,
                 shard,
                 id,
                 price_filter_min,
                 price_filter_max):
        self.price_filter_min = price_filter_min
        self.price_filter_max = price_filter_max
        self.shard = shard
        self.id = id
        self.url = 'https://catalog.wb.ru/catalog/'
        self.query = (f'{self.url}{self.shard}/v2/'
                      'catalog?ab_testing=false'
                      f'&appType=1&cat={self.id}'
                      '&curr=rub'
                      '&dest=-5817685'
                      '&sort=popular'
                      '&spp=30'
                      f'&priceU={price_filter_min*100};{price_filter_max*100}')

    async def prepare_query(self):
        return self.query
