import psycopg2
import time

class Psql_db():
    
    def __init__(self, db_name, user, password, host):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        
    def create_database(self):
            conn = psycopg2.connect(dbname=self.db_name, user=self.user, password=self.password, host=self.host)
            with conn.cursor() as cursor:
                conn.autocommit = True
                try:
                    sql = "CREATE DATABASE wb_parser;"
                    cursor.execute(sql)
                except Exception as ex:
                    print(f'БД существует {ex}')
                    print(f' хотите пересоздать БД?')
                    if input() == 'N':
                        pass 
                    else:
                        conn.close()
                        conn = psycopg2.connect(dbname='postgres', user=self.user, password=self.password, host=self.host)
                        with conn.cursor() as cur:
                            conn.autocommit = True
                            cur.execute("DROP DATABASE wb_parser;")
                            cur.execute("CREATE DATABASE wb_parser;")
            conn.close()  
    
    def create_table(self, name_table):
        self.name_table = name_table
        conn = psycopg2.connect(dbname=self.db_name, user=self.user, password=self.password, host=self.host)
        with conn.cursor() as cursor:
            conn.autocommit = True
            try:
                sql = f"""
                        CREATE TABLE {name_table}
                        (
                            id serial PRIMARY KEY,
                            id_item varchar(200),
                            name varchar(200),
                            brand varchar(200)
                        );
                
                """
                cursor.execute(sql)
            except Exception as ex:
                print(f'Ошибка при создании таблицы - {ex}')
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
    def insert_data(self,list_db):
        conn = psycopg2.connect(dbname=self.db_name, user=self.user, password=self.password, host=self.host)
        with conn.cursor() as cursor:
            conn.autocommit = True
            time_start = time.time()
            for sql in list_db:
                # print(sql)
                cursor.execute(sql[0])
                if not(cursor.fetchall()):
                    cursor.execute(sql[1])
                    #print(f'Выполнена операция INSERT')
                else:
                    cursor.execute(sql[3])
                    if not(cursor.fetchall()):
                        cursor.execute(sql[2])
                        #print(f'Выполнена операция UPDATE')
                    #else:
                        #print(f'Строка существует в БД')
            time_end = time.time()
            print(f'время запроса - {time.gmtime(time_end - time_start)[4]} мин : {time.gmtime(time_end - time_start)[5]} : {time.gmtime(time_end - time_start)[6]}')
        conn.close() 



