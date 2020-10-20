import json
import os
from modules.Database import *
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
import time

load_dotenv()


class Singleton(type):
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(cls, bases, dict)
        cls._instanceDict = {}

    def __call__(cls, *args, **kwargs):
        argdict = {"args": args}
        argdict.update(kwargs)
        argset = frozenset(argdict)
        if argset not in cls._instanceDict:
            cls._instanceDict[argset] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instanceDict[argset]


class DatabaseConnection(metaclass=Singleton):
    def __init__(self):
        self.cnx = None
        self.cur = None
        pass

    def do_connection(self):

        try:
            cnx = mysql.connector.connect(
                user=os.environ["DB_USER"],
                password=os.environ["DB_PWD"],
                host=os.environ["DB_HOST"],
                database=os.environ["DB_NAME"],
                port=os.environ["DB_PORT"],
            )
            print("==== DB CONNECTED ====")
            self.cnx = cnx
            self.cur = cnx.cursor(dictionary=True)
            return cnx
        except mysql.connector.Error as err:
            print("==== DB CONNECTION ERROR ====", err)
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("=== Something is wrong with your user name or password ===")

            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print(" === Database does not exist ===", err)
            else:
                print(" === ERROR ===", err)
                return None

    def close_connection(self):

        self.cnx.close()
        print("====CONNECTION CLOSED====")
        return

    def do_query(self, params):

        try:
            field = params["field"]
            value = params["value"]
            table = params["table"]
            query = "SELECT * FROM `{}` WHERE {} = '{}'".format(table, field, value)
            self.cur.execute(query)
            db_response = self.cur.fetchall()
            return db_response

        except Exception as e:
            print("=== EXCEPTION ===> ", e)

        return
