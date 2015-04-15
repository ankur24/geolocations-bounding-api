import csv
#from pymongo import MongoClient

mongohost = "d7"
mongoport = 27017
#client = MongoClient(mongohost, mongoport)
#db = client.entities
cities = db.cities
docs = [doc for doc in cities.find({"loc": {"$within": {"$box": [[2, 2], [5, 6]]}}})]

#give list geolocation points output
#list of clustered list of geopoints
def cluster(docs):
    pass
