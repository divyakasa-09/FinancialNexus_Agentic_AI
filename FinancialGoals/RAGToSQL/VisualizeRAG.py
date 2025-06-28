import pandas as pd
from Helper.FabricsConnection import get_connection
from Helper.VannaObject import MyVanna
from Helper.Credentials import Credentials
import os
from vanna.flask import VannaFlaskApp

os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Function that takes in a SQL query as a string and returns a pandas dataframe
def run_sql(sql: str):
    df = pd.read_sql_query(sql, conn)
    return df

vn = MyVanna(config={'api_key': Credentials.open_ai_key, 'model': Credentials.model})

# This gives the package a function that it can use to run the SQL
conn = get_connection()
vn.run_sql = run_sql
vn.run_sql_is_set = True
# print(vn.get_training_data())

app = VannaFlaskApp(vn)
app.run()
