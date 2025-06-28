import json
import pandas as pd
from Helper.FabricsConnection import get_connection
from Helper.VannaObject import MyVanna
from Helper.Credentials import Credentials

import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Function that takes in a SQL query as a string and returns a pandas dataframe
def run_sql(sql: str):
    df = pd.read_sql_query(sql, conn)
    return df


def get_ddls():
    file = open('TrainingRAG-Artifact/Tables.json', 'r')
    tables = json.load(file)
    return tables


vn = MyVanna(config={'api_key': Credentials.open_ai_key, 'model': 'gpt-3.5-turbo-16k'})

# This gives the package a function that it can use to run the SQL
conn = get_connection()

vn.run_sql = run_sql
vn.run_sql_is_set = True
#
print("Connection Successfull")
# Training P1
df_information_schema = vn.run_sql("SELECT * FROM INFORMATION_SCHEMA.COLUMNS")
plan = vn.get_training_plan_generic(df_information_schema)

vn.train(plan=plan)
print("Plan trained Successfull")
# Training P2
for query in get_ddls():
    vn.train(ddl = query["query"])

print("DDL trained Successfull")
# Training P3
f = open("TrainingRAG-Artifact/Documentation.txt", "r")
documentation = f.read()

vn.train(documentation = documentation)
print("Documentation trained Successfull")

trained_data = vn.get_training_data()
trained_data.to_csv("training_summary.csv")



