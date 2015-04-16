from flask import Flask
from flask import request,Response
import json
import os

app = Flask(__name__, static_url_path='')


@app.route('/wc/')
def wcroot():
    return app.send_static_file('wordcloud_modular_ec2.html')


@app.route('/')
def indexroot():
    return app.send_static_file('index.html')



#@app.route('/lib/<path:path>')
#def send_foo(path):
#    return send_from_directory('lib', path)

@app.route("/cluster/combined/<brand>/<gram>/")
def hello_combined(brand, gram):
    base = "/home/ubuntu/pythonwebapps/json/"
    with open(base+"combined__themes_output-v2.json", 'r') as f:
        jdict = json.loads(f.read())
        wordlist = jdict[brand][gram]
        text,size = zip(*wordlist)
        size = [ e/10.0 for e in size]
        if gram != 'uni':
            text = map(lambda e: '-'.join(e), text)

        rdict = { 'text': text, 'size': size}
        r = Response(json.dumps(rdict), mimetype='application/json')
        r.headers["Access-Control-Allow-Origin"] = '*'
        return r

    #with open("/home/alok/r-work-dir/topic_models/data_uniTRUE"+i+'.json', 'r') as f:
    #    r = Response(f.read(), mimetype='application/json')
    #    r.headers["Access-Control-Allow-Origin"] = '*'
    #    return r

@app.route("/cluster/lda/<gram>/")
def hello_lda(gram):
    if gram == 'uni':
        whichgram = 'TRUE'
    elif gram == 'bi':
        whichgram = 'FALSE'
    elif gram == 'tri':
        whichgram = "tri"
    fname = "British Gasdata_uni" + whichgram + "1.json"
    base = "/home/alok/r-work-dir/topic_models"
    with open(base + '/' + fname, 'r') as f:
        r = Response(f.read(), mimetype='application/json')
        r.headers["Access-Control-Allow-Origin"] = '*'
        return r

#SSE,nPower
@app.route("/negatives/lda/<gram>/<brand>")
def hello_negative_lda(gram, brand):
    tdict = {'SSE':6,'nPower':4,'British Gas':1}
    if brand == 'BG':
        brand = "British Gas"
    if gram == 'uni':
        whichgram = 'TRUE'
    elif gram == 'bi':
        whichgram = 'FALSE'
    fname = brand+"data_uni"+gram+str(tdict[brand])+ ".json"
    base = "/home/alok/r-work-dir/topic_models/extreme"
    with open(base + '/' + fname, 'r') as f:
        r = Response(f.read(), mimetype='application/json')
        r.headers["Access-Control-Allow-Origin"] = '*'
        return r


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
