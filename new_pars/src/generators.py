from abc import ABC, abstractmethod


class BaseGenerator(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    async def generator(self):
        pass


class CatalogListGenerator(BaseGenerator):

    def __init__(self):
        pass

    async def generator(self,
                        catalog_list):
        for item in catalog_list:
            yield item


class CatalogDataGenerator(BaseGenerator):

    def __init__(self):
        pass

    async def generator(self,
                        catalog_data):
        for catalog in catalog_data:
            yield catalog


class PricePoolGenerator(BaseGenerator):

    def __init__(self,
                 price_start,
                 price_end,
                 price_step):
        self.price_start = price_start
        self.price_end = price_end
        self.price_step = price_step

    async def generator(self):
        for price in range(self.price_start,
                           self.price_end,
                           self.price_step):
            yield price
