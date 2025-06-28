# import pandas as pd
# from Helper.FabricsConnection import get_connection
# from Helper.VannaObject import MyVanna
# from Helper.Credentials import Credentials
# import os

import pandas as pd
from .Helper.FabricsConnection import get_connection
from .Helper.VannaObject import MyVanna
from .Helper.Credentials import Credentials
import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Function that takes in a SQL query as a string and returns a pandas dataframe

def run_sql(sql: str):
    df = pd.read_sql_query(sql, conn)
    return df


def ask_fabric(question):
    global conn
    # vn = MyVanna(config={ 'api_key': Credentials.open_ai_key, 'model': Credentials.model, "visualize": False})
    vn = MyVanna(config={'path': 'FinancialGoals/RAGToSQL/', 'api_key': Credentials.open_ai_key, 'model': Credentials.model, "visualize": False})
    # This gives the package a function that it can use to run the SQL
    conn = get_connection()
    sql = vn.generate_sql(question)

    if "INSERT" in sql:
        cursor = conn.cursor()
        cursor.execute(sql)
        # commit the transaction
        conn.commit()

        return None
    else:
        vn.run_sql = run_sql
        vn.run_sql_is_set = True
        # print(vn.ask(question="Show me the total value of all portfolios managed for each client"))
        data = vn.ask(question=question, visualize=False)

        print(data)

        return data[1].to_dict('records')


# Example usage: Query client portfolio information
# Example: "Fetch all details for a specific client including their portfolios, assets, risk metrics, financial goals, historical projections, and recommended asset allocations."

# Example query for client analysis
example_query = "Fetch all details for client ID 1 including their portfolios, assets, risk metrics, financial goals, historical projections, and recommended asset allocations."
# print(ask_fabric(example_query))
