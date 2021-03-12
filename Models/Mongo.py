import json
from pymongo import MongoClient

# Making Connection
myclient = MongoClient("mongodb://localhost:27017/")

# database
db = myclient["GFG"]

# Created or Switched to collection
# names: GeeksForGeeks
Collection = db["data"]

# Loading or Opening the json file
with open('/Users/prajnyaprabhu/PycharmProjects/MSProject/LiveStream31jul.json') as f:
    file_data = [json.loads(line) for line in f]

# Inserting the loaded data in the Collection
# if JSON contains data more than one entry
# insert_many is used else inser_one is used
if isinstance(file_data, list):
    Collection.insert_many(file_data)
else:
    Collection.insert_one(file_data)