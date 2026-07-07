from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()


class MongoDB:

    def __init__(self):

        self.client = MongoClient(
            os.getenv("MONGO_URI", "mongodb://localhost:27017")
        )

        self.db = self.client[
            os.getenv("DATABASE_NAME", "military")
        ]


    def get_collection(self, collection_name):

        return self.db[collection_name]


    def list_databases(self):

        return self.client.list_database_names()