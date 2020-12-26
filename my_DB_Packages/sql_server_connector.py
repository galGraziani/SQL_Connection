import pandas as pd
from sqlalchemy import create_engine
from faker import Faker
import



class Sql_Server_DataBase:
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
        myDB = pyodbc.connect('Driver={SQL Server};'
                      'Server=server_name;'
                      'Database=database_name;'
                      'Trusted_Connection=yes;')

        return myDB

    def queryToPandas(self, query):
        df = pd.read_sql_query(query, self.engine)
        return df

    def sendQuery(self, query):
        myCursor = self.myDB.cursor()
        myCursor.execute(query)