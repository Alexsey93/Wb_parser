import psycopg2.extras
import requests
import json
from psycopg2.extras import Json

# conn = psycopg2.connect(dbname='wb_parser', user='alex', password='afbdogs', host='212.26.248.159')
# with conn.cursor() as cursor:
#     conn.autocommit = True
#     sql1 = f"SELECT * FROM test;"
#     sql2 = f"INSERT INTO test (id) VALUES('1');"
#     test_sql = f"CREATE TABLE IF NOT EXISTS test(id varchar(30));" + sql2 + sql1
#     print(test_sql)
#     cursor.execute(test_sql)
#     print(cursor.fetchall())
# conn.close()
# # print(str(  (
#                                 (f"SELECT * FROM All_items WHERE EXISTS(SELECT * FROM All_items WHERE id_item='');"),
#                                 (f"INSERT INTO All_items (id_item, name, brand) VALUES ('','','');"),
#                                 (f"UPDATE All_items SET name='',brand='' WHERE id_item='';"),
#                                 (f"SELECT * FROM All_items WHERE EXISTS(SELECT * FROM All_items WHERE id_item='' AND name='' AND brand='');"),
#                                 ) ))
# test = []
# test.append((1,1,1))
# print(test)
# test.append((2,2,2))
# print(f"{test}")
# test_l = []
# test = [i for i in range (5000)]
# i = 0
# while i < 5000:
#     test_l = test[i:i+100]
#     i += 100
#     print(test_l,'\n')
json_sql = {}
table_name = 'item_cat'
column_name = 'name_cat_item,json_cat'
values = f"'bl_shirts',"
def json_to_db(json_sql, table_name, column_name, values):
        conn = psycopg2.connect(dbname='wb_parser', user='alex', password='afbdogs', host='212.26.248.159')
        conn.autocommit = True
        with conn.cursor() as cursor:
            sql = f"INSERT INTO {table_name} ({column_name}) VALUES ({values}%s);"
            print(sql)
            cursor.execute(sql, [Json(json_sql)])

json_to_db(json_sql, table_name, column_name, values)