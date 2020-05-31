import psycopg2 as pg
import logging as lg

import sys
import os
import time

DEBUG = True if "DEBUG" not in os.environ else bool(int(os.environ["DEBUG"]))

class ShopDatabase:
    def __init__(self):
        lg.info("AUTH: in __init__", file=sys.stderr)
        success = False
        while not success:
          try:
            if (DEBUG):
                self.connection = pg.connect(
                    host="localhost",
                    #port="5234",
                    user="postgres",
                    password="postgres",
                    dbname="ShopOnTheCoach"
                )
            else:
                print("AUTH INITED INSIDE CONTAINER", file=sys.stderr)
                self.connection = pg.connect(
                    host="db",
                    #port="5234",
                    user="postgres",
                    password="postgres",
                    dbname="Shop"
                )
            self.cursor = self.connection.cursor()
            lg.info("Starting initialization")
            self.__db_init()
            success = True
          except:
            print("AUTH: Failed to connect. Retry", file=sys.stderr)
            time.sleep(10)

    def __db_init(self):
        check_request = '''
            SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA;
        '''
        x = set(x[0] for x in self.read(check_request))
        
        if ('users' not in x):
            init_request_1 = """
                CREATE SCHEMA users;
                ALTER SCHEMA users OWNER TO postgres;
            """
            self.execute(init_request_1, "Creating Users")
        
        #  Users check
        check_request_users = '''
        SELECT EXISTS (
           SELECT 1
           FROM   information_schema.tables
           WHERE  table_schema = 'users'
           AND    table_name = 'users'
           );
        '''
        iteminfo_exists = self.read(check_request_users)[0][0]
        print("AUTH: Users", iteminfo_exists, file=sys.stderr)
        if (not iteminfo_exists):
            init_request_table_1 = """
                CREATE TABLE users.users (
                    login text,
                    password text,
                    email text,
                    DistributorID integer DEFAULT null,
                    role varchar(12) DEFAULT 'user'
                );
            """
            self.execute(init_request_table_1, "Creating users.users")
        
        #  Tokens check
        check_request_users = '''
        SELECT EXISTS (
           SELECT 1
           FROM   information_schema.tables
           WHERE  table_schema = 'users'
           AND    table_name = 'tokens'
           );
        '''
        iteminfo_exists = self.read(check_request)[0][0]
        print("AUTH: Tokens", iteminfo_exists, file=sys.stderr)
        if (not iteminfo_exists):
            init_request_table_2 = """
                CREATE TABLE users.tokens (
                    'login' text,
                    'refresh_token' text,
                    'access_token' text,
                );
            """
            self.execute(init_request_table_2, "Creating users.tokens")
        
        #  distributors check
        check_request_users = '''
        SELECT EXISTS (
           SELECT 1
           FROM   information_schema.tables
           WHERE  table_schema = 'users'
           AND    table_name = 'distributors'
           );
        '''
        iteminfo_exists = self.read(check_request)[0][0]
        print("AUTH: Distributors", iteminfo_exists, file=sys.stderr)
        if (not iteminfo_exists):
            init_request_table_3 = """
                CREATE TABLE users.distributors (
                    'DistributorName' text NOT NULL,
                    'DistributorID' int NOT NULL,
                );
            """
            self.execute(init_request_table_3, "Creating users.distributors")

    def execute(self, request, message=""):
        lg.info("Выполняю запрос" 
                "" if not message else "<{}>".format(message))
        try:
            self.cursor.execute(request)
            self.connection.commit()
        except pg.DatabaseError as err:
            lg.error(err)
            self.connection.rollback()
        else:
            lg.info("Закончил запрос"
                    "" if not message else "<{}>".format(message))

    def read(self, request, message=""):
        lg.info("Выполняю запрос"
                "" if not message else "<{}>".format(message))
        returned = ()
        try:
            self.cursor.execute(request)
            returned = self.cursor.fetchall()
            self.connection.commit()

        except pg.DatabaseError as err:
            lg.error(err)
            self.connection.rollback()
        lg.info("Закончил запрос"
                "" if not message else "<{}>".format(message))
        return returned
