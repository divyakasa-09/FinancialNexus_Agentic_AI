from Helper.VannaObject import MyVanna
import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"

vn = MyVanna(config={'api_key': 'enter-api-key', 'model': 'gpt-3.5-turbo-16k'})

# print(vn.get_training_data())

print(vn.generate_sql("Tell me the top 3 client with highest portfolio."))




