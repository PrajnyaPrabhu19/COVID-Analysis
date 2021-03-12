from geopy.geocoders import Nominatim
from pymongo import MongoClient

myclient = MongoClient("mongodb://localhost:27017/")
db = myclient["GFG"]
collec = db["data"]
geolocator = Nominatim(user_agent="geoapiExercises")

results = collec.find({"$where":"function()"
                                "{geolocator = Nominatim(user_agent='geoapiExercises')"
                                "return ('India' in (geolocator.geocode(this.user.location)))}"})


for item in results:
    print(item)
    new_data = []
    new_data.append(item['extended_tweet']['full_text'])

print("lenght: ",len(new_data))