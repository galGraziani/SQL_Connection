import pandas as pd
from pandas import ExcelWriter
import openpyxl
import xlrd
from my_DB_Packages.mysql_db_connector import Mysql_DataBase

DB_For_Project = Mysql_DataBase("localhost", "root", "Bg8187915", "DB_For_Project", "3306")


# Function to save each year on different sheets
def save_xls(list_dfs, xls_path, name_of_sheets):
    with ExcelWriter(xls_path) as writer:
        for n, df in enumerate(list_dfs):
            df.to_excel(writer, name_of_sheets[n])
        writer.save()


def get_Table_As_DF(query):
    table_df = DB_For_Project.queryToPandas(query)

    return table_df

def get_List_Of_Tables_df():
    lst = get_List_Of_tables()
    list_of_df = []
    for table in range(len(lst)):
        query = 'SELECT * FROM ' + str(lst[table]) + ';'
        list_of_df.append(get_Table_As_DF(query))
    return list_of_df

def get_List_Of_tables():
    tables = DB_For_Project.queryToPandas('SHOW TABLES')
    return tables['Tables_in_db_for_project'].tolist()

list_of_df = get_List_Of_Tables_df()

save_xls(list_of_df, 'blabla.xlsx', get_List_Of_tables())

# get_List_Of_df(['cusomers', ])
