from flask import Flask
from flask import request,Response
import json
import os
from sklearn import cluster
from sklearn.neighbors import kneighbors_graph
from sklearn.preprocessing import StandardScaler
from pymongo import MongoClient, GEO2D
import numpy as np
import collections

app = Flask(__name__, static_url_path='')

def pool(docsa, y_pred):
    tens = collections.defaultdict(lambda: [[0,0],0])
    for i in xrange(len(docs)):
        tens[y_pred[i]][0][0] += docs[i][0]
        tens[y_pred[i]][0][1] += docs[i][1]
        tens[y_pred[i]][1] += 1
    return tens

@app.route("/api/points", methods=['get')
def getclusteredpoints(brand, gram):
    try:
        bl = map(float, request.form['bl'].split(','))
        tr = map(float, request.form['tr'].split(','))
    except:
        return Response('{}', mimetype='application/json', headers={"Access-Control-Allow-Origin":'*'})
    client = MongoClient("mongodb://u:p@ds049170.mongolab.com:49170/commondb")
    db = client.commondb
    cities = db.cities
    
    
    #docs = [doc['loc'] for doc in cities.find({"loc": {"$geoWithin": {"$box": [[1.5, 42], [2, 45]]}}})]
    docs = [doc['loc'] for doc in cities.find({"loc": {"$geoWithin": {"$box": [bl, tr]}}})]
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
        rjsonobj = pool(docs, y_pred)
    else:
        rjsonobj = print zip(docs, 0*len(docs))
    r = Response(json.dumps(rjsonobj), mimetype='application/json')
    r.headers["Access-Control-Allow-Origin"] = '*'
    return r


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
