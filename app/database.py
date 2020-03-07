import psycopg2 as pg
import logging as lg

class ShopDatabase:
    def __init__(self):
        self.connection = pg.connect(
            host="localhost", 
            user="postgres", 
            password="postgres", 
            dbname="ShopOnTheCoach"
        )
        self.cursor = self.connection.cursor()
    
    def execute(self, request, message=""):
        lg.info("Выполняю запрос" \
                "" if not message else "<{}>".format(message))
        try:
            self.cursor.execute(request)
            self.connection.commit()
        except pg.DatabaseError as err:       
            lg.error(err)
            self.connection.rollback()
        else:
            lg.info("Закончил запрос" \
                "" if not message else "<{}>".format(message))
    
    def read(self, request, message=""):
        lg.info("Выполняю запрос" \
                "" if not message else "<{}>".format(message))
        returned = ()
        try:
            self.cursor.execute(request)
            returned = self.cursor.fetchall() 
            self.connection.commit()
            
        except pg.DatabaseError as err:       
            lg.error(err)
            self.connection.rollback()
        lg.info("Закончил запрос" \
                "" if not message else "<{}>".format(message))
        return returned



    