from pymongo import MongoClient
from math import radians, cos, sin, asin, sqrt
import json

client = MongoClient(port=27017)
db = client['drugi_kolokvijum']
cities_collection = db['cities']
streets_collection = db['streets']

center_point = {'lat': 44.756957, 'lon': 19.212933}

cities_cursor = cities_collection.find()

cities_list = list(cities_cursor)

cities_clean = []


def haversine(lon1, lat1, lon2, lat2):

    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371
    return c * r


for city in cities_list:

    cities_clean.append({'name': city['name']})


with open('cities.json', 'w') as file:
    json.dump(cities_clean, file)


streets_cursor = streets_collection.find()

streets_list = list(streets_cursor)

streets_within = []


for street in streets_list:

    isWithin = False

    if(street['city'] == 'Bijeljina'):
        if len(street['locations']) > 0:
            for location in street['locations']:

                test_point = {'lat': float(
                    location['lat']), 'lon': float(location['lon'])}

                radius = 3
                c = haversine(
                    center_point['lat'], center_point['lon'], test_point['lat'], test_point['lon'])

                if(c <= radius):
                    isWithin = True

        if isWithin == True:
            print(street)
            streets_within.append(
                {'city': street['city'], 'street': street['street']})



with open('streetsWithinRadius.json', 'w') as file:
    json.dump(streets_within, file)
