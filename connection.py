from FinancialGoals.RAGToSQL.Helper.Credentials import Credentials

# Get the token
# Retrive the Token Value for your login
from azure.identity import InteractiveBrowserCredential
credential = InteractiveBrowserCredential()
#
# Once retrived copy the token value
token_object = credential.get_token(Credentials.resource_url)
print(token_object.token)

