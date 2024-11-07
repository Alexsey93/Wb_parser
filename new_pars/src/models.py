from sqlalchemy import Table, Column, Integer
from sqlalchemy import String, MetaData


metadata_obj = MetaData()

category_table = Table(
    "Categories",
    metadata_obj,
    Column('id',
           Integer,
           primary_key=True,
           ),
    Column('name',
           String,
           ),
    Column('id_cat',
           Integer,
           ),
    Column('shard',
           String,
           )
    )

items_table = Table(
    "Items",
    metadata_obj,
#     Column('id_table',
#            Integer,
#            primary_key=True
#            ),
    Column('id',
           Integer
           ),
    Column('brand',
           String,
           ),
    Column('name',
           String,
           )
)
