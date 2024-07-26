# from pymongo import MongoClient

# def get_db():
#     # Replace the URI with your MongoDB deployment's connection string
#     client = MongoClient('mongodb://localhost:27017/')
#     db = client['chat_db']
#     return db

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = "mongodb+srv://islamtalha01:talha4655@cluster0.i5qr0eq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server


def get_db():
   client = MongoClient(uri, server_api=ServerApi('1'))
   db = client['chat_db']
   return db