
#docs = [doc for doc in cities.find({"loc": {"$within": {"$box": [[2, 2], [5, 6]]}}})]

#docs = [doc for doc in cities.find({"loc": {"$geoWithin": {"$box": [[2, 2], [5, 6]]}}})]

#give list geolocation points output
#list of clustered list of geopoints
from sklearn import cluster
from pymongo import MongoClient, GEO2D
import numpy as np
import collections

#mongohost = "ds049170.mongolab.com:49170/commondb"
#mongoport = 49170
client = MongoClient("mongodb://user:pass@ds049170.mongolab.com:49170/commondb")
db = client.commondb
cities = db.cities

docs = [doc.loc for doc in cities.find({"loc": {"$geoWithin": {"$box": [[1.5, 42], [2, 45]]}}})]
#print docs
if len(docs) > 10:
    #docsa =np.array(docs)
    # normalize dataset for easier parameter selection
    X = StandardScaler().fit_transform(docs)
    # connectivity matrix for structured Ward
    connectivity = kneighbors_graph(X, n_neighbors=10, include_self=False)
    # make connectivity symmetric
    connectivity = 0.5 * (connectivity + connectivity.T)
    average_linkage = cluster.AgglomerativeClustering(
        linkage="average", affinity="cityblock", n_clusters=10,
        connectivity=connectivity)
    average_linkage.fit(docs)
    y_pred = average_linkage.labels_.astype(np.int)
    print pool(docs, y_pred)
else:
    print zip(*docs, 0*len(docs))

def pool(docsa, y_pred):
    tens = collections.defaultdict(labmda: [0,0,0])
    for i in len(docs):
        tens[y_pred[i]][0] += docs[i][0]
        tens[y_pred[i]][1] += docs[i][1]
        tens[y_pred[i]][1] += 1
    return tens
