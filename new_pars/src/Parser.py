from abc import ABC, abstractmethod


class Parser(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    async def get_cat_info():
        pass


class ParserCatalog(Parser):

    def __init__(self):
        self.cat_data = None

    async def get_cat_info(self, data=None, list_cat=None):
        dict_info_category = {}
        if list_cat is None:
            list_cat = []
        if isinstance(data, list):
            for category in data:
                # print(f'-----\n\n\n{category}\n\n\n-----')
                await self.get_cat_info(data=category,
                                        list_cat=list_cat)
        elif isinstance(data, dict):
            if 'childs' in data:
                # print(f'\n\n\n{data.get('childs')}\n\n\n')
                await self.get_cat_info(data=data.get('childs'),
                                        list_cat=list_cat)
            else:
                if data.get('shard'):
                    if data.get('shard') != 'blackhole':
                        dict_info_category[data.get('name')] = [data.get('shard'),
                                                                data.get('id')]
                        list_cat.append(dict_info_category)
        self.cat_data = list_cat
        return list_cat
