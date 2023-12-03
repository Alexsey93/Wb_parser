import psycopg2

conn = psycopg2.connect(dbname='wb_parser', user='alex', password='afbdogs', host='212.26.248.159')
with conn.cursor() as cursor:
    conn.autocommit = True
    sql = "SELECT * FROM test WHERE EXISTS( SELECT * FROM test WHERE id='1');"
    cursor.execute(sql)
    print(bool(cursor.fetchall()))
conn.close()