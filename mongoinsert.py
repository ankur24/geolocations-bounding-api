import csv
from pymongo import MongoClient

mongohost = "d7"
mongoport = 27017
client = MongoClient(mongohost, mongoport)
db = client.entities
cities = db.cities 
cities.create_index([("loc", GEO2D)])
with open('wcp.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print float(row['Longitude']),float(row['Latitude'])
        row['loc'] = [float(row['Longitude']),float(row['Latitude'])]
        del row['Longitude']
        del row['Latitude']
        #db.cities.insert_one(row)
        break
