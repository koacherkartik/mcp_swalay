try:
    from pymongo import MongoClient
except ImportError as exc:
    raise ImportError("pymongo is not installed. Install it with 'pip install pymongo'.") from exc

client = MongoClient("mongodb://localhost:27017")

print("Connected Successfully")

print()

print(client.list_database_names())