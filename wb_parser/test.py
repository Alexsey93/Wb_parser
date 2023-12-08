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

def json_to_sql():
        dict_info_d = {}
        conn = psycopg2.connect(dbname='wb_parser', user='alex', password='afbdogs', host='212.26.248.159')
        with conn.cursor() as cursor:
            conn.autocommit = True
            test_table = f"""
                        CREATE TABLE IF NOT EXISTS test
                            (
                                test_json jsonb    
                            );
            
            """
            cursor.execute(test_table)
            with open ('data/menu.json', encoding="utf-8") as f:
                name = json.load(f)
                sql = f"""
                        INSERT INTO test (test_json) VALUES (%s) ON CONFLICT DO NOTHING returning test_json
                """
                cursor.execute(sql, [Json(name)])
                # cursor.execute("SELECT (test_json[0] -> 'childs')[0] -> 'id' FROM test;")
                # print(cursor.fetchall())
                cursor.execute("SELECT test_json FROM test;")
                sql_json =(cursor.fetchall()[0])
                sql_json = json.loads(json.dumps(sql_json))
                for cat in sql_json[0]:
                    if not('shard' in cat):
                        if 'childs' in cat:
                            for child in cat['childs']:
                                if 'shard' in child:
                                    print(child, '\n')
                                    dict_info_d[child['shard']] = [child['id'],child['name']]
                    elif cat['shard'] == 'blackhole':
                        for child in cat['childs']:
                            if 'shard' in child:
                                dict_info_d[child['shard']] = [child['id'],child['name']]
                print(dict_info_d)
        conn.close()
json_to_sql()