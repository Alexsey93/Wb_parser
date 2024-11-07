import asyncio
from unicodedata import category
import asyncpg
from .models import metadata_obj, category_table, items_table
from ..config import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import session, sessionmaker
from sqlalchemy import URL, create_engine, text, insert
from abc import ABC, abstractmethod
from .Logger import ResponseLogger


class PostgresBase(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    async def pg_client(self):
        pass


class Postgres(PostgresBase):

    def __init__(self):
        logger = ResponseLogger()
        self.log = logger.log

    async def pg_client(self):
        engine = create_async_engine(
                url=settings.DATABASE_URL_asyncpg,
                echo=True,
        )
        async with engine.begin() as conn:
            await self.create_table(conn=conn)

    async def create_table(self,
                           conn):
        await conn.run_sync(metadata_obj.drop_all)
        await conn.run_sync(metadata_obj.create_all)

    async def insert_to_bd(self,
                           query
                           ):
        engine = create_async_engine(
                url=settings.DATABASE_URL_asyncpg,
                echo=True,
        )
        async with engine.begin() as conn:
            await self.create_table(conn=conn)
            await conn.execute(query)

    async def query_bd_cat(self,
                           data,
                           table):
        stmt = insert(table).values(data)
        return stmt
    # async def pg_client(self):
    #     engine = create_async_engine(
    #         url=settings.DATABASE_URL_asyncpg,
    #         echo=True,

    #     )
    #     self.log.info(settings.DATABASE_URL_asyncpg)
    #     return engine
        # conn = await asyncpg.connect(user='postgres',
        #                              password='wb_base',
        #                              database='postgres',
        #                              host='10.0.100.10')
        # cursor = conn.
        # values = await conn.fetch('''SELECT * FROM mytable''')
        # print(values)
        # self.log.info(f'----------------------{values}--------------------')
