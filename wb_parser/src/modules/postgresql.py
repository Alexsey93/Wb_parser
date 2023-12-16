import psycopg2
# import time
from psycopg2.extras import Json

class Psql_db():
    
    def __init__(self, db_name, user, password, host):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        
            
    def set_sql_request(self, sql_request):
        conn = psycopg2.connect(dbname=self.db_name, user=self.user, password=self.password, host=self.host)
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute(sql_request)
        conn.close()
        
    def get_sql_response(self, sql_request):
        conn = psycopg2.connect(dbname=self.db_name, user=self.user, password=self.password, host=self.host)
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute(sql_request)
            request = cursor.fetchall()
        conn.close()
        return request
    
    def create_table(self, name_table, field_table):
        conn = psycopg2.connect(dbname=self.db_name, user=self.user, password=self.password, host=self.host)
        conn.autocommit = True
        with conn.cursor() as cursor:
            try:
                sql = f"CREATE TABLE {name_table} ({field_table});"
                cursor.execute(sql)
            except Exception as ex:
                print(f'Ошибка при создании таблицы \n {ex}')
        conn.close()
    
    def create_database(self):
        try:
            conn = psycopg2.connect(dbname=self.db_name, user=self.user, password=self.password, host=self.host)
            conn.autocommit = True
            with conn.cursor() as cursor:
                sql = "CREATE DATABASE wb_parser;"
                cursor.execute(sql)
        except Exception as ex:
            print(f'произошла ошибка \n {ex}\n Попытка пересоздать БД \n')
            try:
                conn = psycopg2.connect(dbname='postgres', user=self.user, password=self.password, host=self.host)
                conn.autocommit = True
                with conn.cursor() as cursor:
                    sql = "CREATE DATABASE wb_parser;"
                    cursor.execute(sql)
            except Exception as ex:
                print(f'произошла ошибка \n {ex}\n Попытка пересоздать БД \n')
            finally:
                conn.close()
        finally:
            conn.close()
    
    def json_to_db(self, json_sql, table_name, column_name, values, unique_field, update_field):
        conn = psycopg2.connect(dbname=self.db_name, user=self.user, password=self.password, host=self.host)
        conn.autocommit = True
        with conn.cursor() as cursor:
            sql = f'INSERT INTO {table_name} ({column_name}) VALUES ({values}%s) ON CONFLICT ({unique_field}) DO UPDATE SET {update_field}=%s;'
            cursor.execute(sql, [Json(json_sql),Json(json_sql)])
        conn.close()
        
    def db_to_json(self,column_name, table_name):
        conn = psycopg2.connect(dbname=self.db_name, user=self.user, password=self.password, host=self.host)
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT {column_name} FROM {table_name};")
            self.sql_json =(cursor.fetchall()[0])
        conn.close()
        return self.sql_json
        
    def create_schemas(self, name_schemas):
        conn = psycopg2.connect(dbname=self.db_name, user=self.user, password=self.password, host=self.host)
        conn.autocommit = True
        with conn.cursor() as cursor:
            try:
                sql=f'CREATE SCHEMA IF NOT EXISTS {name_schemas};'
                cursor.execute(sql)
            except Exception as exception:
                print(f'{exception}')
            finally: 
                conn.close()   
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    # def insert_data(self,id_item, name_item, brand):
    #     symb = ['/','\\','.',' ','-','\'']
    #     for sym in symb:
    #         if sym in name_item:
    #             name_item = name_item.replace(sym,'_')
    #         if sym in brand:
    #             brand = brand.replace(sym,'_')
    #     conn = psycopg2.connect(dbname=self.db_name, user=self.user, password=self.password, host=self.host)
    #     with conn.cursor() as cursor:
    #         conn.autocommit = True
    #         sql = f"""
    #                 INSERT INTO {self.name_table}(id_item, name, brand) VALUES ({id_item},'{name_item}','{brand}');
    #         """
    #         cursor.execute(sql)
    #     conn.close() 
    # def insert_data(self,list_db):
    #     conn = psycopg2.connect(dbname=self.db_name, user=self.user, password=self.password, host=self.host)
    #     with conn.cursor() as cursor:
    #         conn.autocommit = True
    #         time_start = time.time()
    #         for sql in list_db:
    #             # print(sql)
    #             cursor.execute(sql[0])
    #             if not(cursor.fetchall()):
    #                 cursor.execute(sql[1])
    #                 #print(f'Выполнена операция INSERT')
    #             else:
    #                 cursor.execute(sql[3])
    #                 if not(cursor.fetchall()):
    #                     cursor.execute(sql[2])
    #                     #print(f'Выполнена операция UPDATE')
    #                 #else:
    #                     #print(f'Строка существует в БД')
    #         time_end = time.time()
    #         print(f'время запроса - {time.gmtime(time_end - time_start)[4]} мин : {time.gmtime(time_end - time_start)[5]} : {time.gmtime(time_end - time_start)[6]}')
    #     conn.close() 



