# import psycopg2

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
res = []
id = 'is'
name = 'this'
name_2 = 'string'
res.append((id,name,name_2))
res_str = ''.join(str(e) for e in res) + ',' 
print(res_str)