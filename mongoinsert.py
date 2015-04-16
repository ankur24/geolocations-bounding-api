import csv
from pymongo import MongoClient, GEO2D

#mongohost = "ds049170.mongolab.com:49170/commondb"
#mongoport = 49170
client = MongoClient("mongodb://user:pass@ds049170.mongolab.com:49170/commondb")
db = client.commondb
cities = db.cities
temp = []
with open('wcp.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for i,row in enumerate(reader):
        #if i <= 1000: continue
        row['loc'] = [float(row['Longitude']),float(row['Latitude'])]
        del row['Longitude']
        del row['Latitude']
        temp.append(row)
        if i % 50 == 0:
            db.cities.insert(temp)
            temp = []
        #print float(row['Longitude']),float(row['Latitude'])
        #break
        #if i > 1000: break
    if temp:
        db.cities.insert(temp)
cities.create_index([("loc", GEO2D)])
