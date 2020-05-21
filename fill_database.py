import xml.etree.ElementTree as ET
from pymongo import MongoClient

client = MongoClient(port=27017)
db = client['drugi_kolokvijum']
cities_collection = db['cities']
streets_collection = db['streets']

cities_collection.delete_many({})
streets_collection.delete_many({})

all_streets = []
all_cities = []
cities_list = []

filename = 'bosnia-herzegovina-latest.osm'


tag_keys = {}
tags = {}
cities = {}
streets = {}
locations = {}
count = 0
for event, elem in ET.iterparse(filename):
    city = None
    street = None
    location = None
    for ee in elem:
        for atrelem in ee.attrib:
            for key in ee.attrib:
                if key == 'k':
                    key_value = ee.attrib[key]
                    if key_value not in tag_keys:
                        tag_keys[key_value] = 0
                    tag_keys[key_value] += 1

            if 'k' in ee.attrib and 'v' in ee.attrib:
                key = ee.attrib['k']
                value = ee.attrib['v']
                if key == 'addr:city':
                    city = value
                if key == 'addr:street':
                    street = value
    if city is not None and street is not None:
        if city not in cities:
            cities[city] = 0
        cities[city] += 1
        addr = city + '\t'+street
        if addr not in streets:
            streets[addr] = 0
            locations[addr.split('\t')[1]] = []
            if(elem.attrib.get('lat') is not None and elem.attrib.get('lon') is not None):
                locations[addr.split('\t')[1]].append(
                    {'lat': float(elem.attrib.get('lat')), 'lon': float(elem.attrib.get('lon'))})


        streets[addr] += 1
        if(elem.attrib.get('lat') is not None and elem.attrib.get('lon') is not None):
            locations[addr.split('\t')[1]].append(
                {'lat': elem.attrib.get('lat'), 'lon': elem.attrib.get('lon')})

    if elem.tag not in tags:
        tags[elem.tag] = 0
    tags[elem.tag] += 1

    if count % 100000 == 0:
        stag = [[k, v] for k, v in sorted(
            tag_keys.items(), key=lambda item: item[1], reverse=True)]

        scities = [[k, v] for k, v in sorted(
            cities.items(), key=lambda item: item[1], reverse=True)]
        with open('cities.txt', 'w') as file:
            for el in scities:
                cities_list.append(el[0])

        sstreets = [[k, v] for k, v in sorted(
            streets.items(), key=lambda item: item[1], reverse=True)]
        with open('streets.txt', 'w') as file:
            for el in sstreets:
                arr = el[0].split('\t')
                city = arr[0]
                street = arr[1]
                all_streets.append(
                    {'city': city, 'street': street, 'locations': locations[street]})

    if event == 'end' and elem.tag in ['node', 'way', 'relation']:
        elem.clear()
    count += 1
    if count > 60000000:
        break

cities_list = list(set(cities_list))
for i in cities_list:
    all_cities.append({'name': i})

seen_streets = set()
new_list = []
for obj in all_streets:
    if obj.get('street')+obj.get('city') not in seen_streets:
        new_list.append(obj)
        seen_streets.add(obj.get('street')+obj.get('city'))

cities_collection.insert_many(all_cities)
streets_collection.insert_many(new_list)

