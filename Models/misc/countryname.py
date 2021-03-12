from geopy.geocoders import Nominatim
from pymongo import MongoClient

def countryName(location):
    geolocator = Nominatim(user_agent="geoapiExercises")
    try:
        country = geolocator.geocode(location)
        if(country == None):
            return False
        if('India' in country):
            return True
        else:
            return False
    except:
        print("geocodeexcpt")


myclient = MongoClient("mongodb://localhost:27017/")
db = myclient["GFG"]
collec = db["data"]

#results= collec.find({"user.location":{"$ne":'null'}},{'user.location':1,'extended_tweet.full_text':1})
results= collec.find({"user.location":{"$exists":True}})
extra =[]
new_data=[]
list_of_strings = ['india', 'bharat','indian']

for item in results:
    #print(item)
    try:
        if (countryName(item['user']['location'])):
            if item['extended_tweet'] is None:
                extra.append(item)
            else:
                new_data.append(item['extended_tweet']['full_text'])
    except KeyError:
        print("keynotfound")
    except:
        print("exhaust")

print("length:",len(new_data))

#        else:
#           for string in list_of_strings:
 #               if(item['user']['location']==None):
  #                  extra.append(item)
   #                 break;
    #            else:
     #               if(string in item['user']['location']):
      #                  if item['extended_tweet'] is None:
       #                     extra.append(item)
        #                    break
         #               else:
          #                  new_data.append(item['extended_tweet']['full_text'])
           #                 break