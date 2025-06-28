
import struct
from itertools import chain, repeat
import pyodbc
from .Credentials import Credentials

# Get the token
# Retrive the Token Value for your login
# from azure.identity import InteractiveBrowserCredential
# credential = InteractiveBrowserCredential()
#
# Once retrived copy the token value
# token_object = credential.get_token(Credentials.resource_url)
# print(token_object.token)

def get_connection():
    # Make connection string
    connection_string = f"Driver={{ODBC Driver 18 for SQL Server}};Server={Credentials.sql_endpoint},1433;Database=f{Credentials.database};Encrypt=Yes;TrustServerCertificate=No"
    # Set Token Values
    token_as_bytes = bytes(Credentials.token, "UTF-8")  # Convert the token to a UTF-8 byte string
    encoded_bytes = bytes(
        chain.from_iterable(zip(token_as_bytes, repeat(0))))  # Encode the bytes to a Windows byte string
    token_bytes = struct.pack("<i", len(encoded_bytes)) + encoded_bytes  # Package the token into a bytes object
    attrs_before = { 1256: token_bytes }  # Attribute pointing to SQL_COPT_SS_ACCESS_TOKEN to pass access token to the driver
    # Connect with PYODBC
    connection = pyodbc.connect(connection_string, attrs_before=attrs_before)
    return connection