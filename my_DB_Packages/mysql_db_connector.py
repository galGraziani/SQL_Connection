import mysql.connector
import pandas as pd
from sqlalchemy import create_engine
from faker import Faker


class Mysql_DataBase:
    def __init__(self, host, userName, password, dbName, port):
        self.host = host
        self.userName = userName
        self.password = password
        self.port = port
        self.dbName = dbName
        self.engine = self.getEngine()
        self.myDB = self.getConnection()


    def getEngine(self):
        engine = create_engine("mysql+pymysql://" +
                               self.userName + ":" +
                               self.password + "@" +
                               self.host + ":" +
                               self.port + "/DB_For_Project")
        return engine

    def getConnection(self):
        myDB = mysql.connector.connect(
            host=self.host,
            user=self.userName,
            password=self.password,
            database=self.dbName
        )
        return myDB

    def queryToPandas(self, query):
        df = pd.read_sql_query(query, self.engine)
        return df

    def sendQuery(self, query):
        myCursor = self.myDB.cursor()
        myCursor.execute(query)