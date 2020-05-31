import psycopg2 as pg
import logging as lg
import os
import time

DEBUG = True if "DEBUG" not in os.environ else bool(int(os.environ["DEBUG"]))

class ShopDatabase:
    def __init__(self):
        lg.info("in __init__")
        if (DEBUG):
            self.connection = pg.connect(
                host="localhost",
                #port="5234",
                user="postgres",
                password="postgres",
                dbname="ShopOnTheCoach"
            )
        else:
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

    def __db_init(self):
        check_request = '''
            SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA;
        '''
        x = set(x[0] for x in self.read(check_request))
        if ('items' not in x):
            init_request_1 = """
                CREATE SCHEMA items;
                ALTER SCHEMA items OWNER TO postgres;
            """
            self.execute(init_request_1, "Creating Items")
        
        check_request = '''
        SELECT EXISTS (
           SELECT 1
           FROM   information_schema.tables
           WHERE  table_schema = 'items'
           AND    table_name = 'iteminfo'
           );
        '''
        iteminfo_exists = self.read(check_request)[0][0]
        if (not iteminfo_exists):
            init_request_2 = """
                CREATE TABLE items.iteminfo (
                    "ItemName" text NOT NULL,
                    "EAN" bigint NOT NULL,
                    category character varying(30),
                    id integer NOT NULL,
                    distributorID integer
                );
                ALTER TABLE ONLY items.iteminfo
                    ADD CONSTRAINT iteminfo_pk PRIMARY KEY ("EAN");
                ALTER TABLE items.iteminfo OWNER TO postgres;
                COMMENT ON TABLE items.iteminfo IS 'Information about items';
                CREATE SEQUENCE items.iteminfo_id_seq
                    AS integer
                    START WITH 1
                    INCREMENT BY 1
                    NO MINVALUE
                    NO MAXVALUE
                    CACHE 1;
                ALTER TABLE items.iteminfo_id_seq OWNER TO postgres;
                ALTER SEQUENCE items.iteminfo_id_seq OWNED BY items.iteminfo.id;
                ALTER TABLE ONLY items.iteminfo ALTER COLUMN id SET DEFAULT nextval('items.iteminfo_id_seq'::regclass);
            """
            self.execute(init_request_2, "Configuring Items.Items")
            init_migration_1 = """
                INSERT INTO items.iteminfo ("ItemName", "EAN", category) VALUES 
                    ('Сыр', 2,  'Продукты'),
                    ('Колбаса сырокопчёная',    13, 'Продукты'),
                    ('Тапочки чёр.',    103,    'Обувь'),
                    ('Кабачки вяленые', 19, 'Продукты'),
                    ('Валенки', 133,    'Обувь'),
                    ('Кукуруза',    105,    'Продукты'),
                    ('Тапочки', 102,    'Консервы'),
                    ('Пуговица',    202,    'Одежда')
            """
            self.execute(init_migration_1, "Making migration to Items.Items")
        
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
