from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="geoapiExercises")
location = geolocator.geocode("kumta")
print("Country Name: ", location)



list_of_strings = ['india', 'bharat','indian']

print(list_of_strings)

#country_in_list= ((string for string in list_of_strings) in 'bengaluru, india, world')

#for string in list_of_strings:
#    country_in_list = string in 'bengaluru, india, world'
#    if(country_in_list):
 #       break

#print(country_in_list)