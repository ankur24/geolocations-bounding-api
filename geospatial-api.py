from flask import Flask
from flask import request,Response
import json
import os

app = Flask(__name__, static_url_path='')


@app.route('/')
def root():
    return app.send_static_file('wordcloud_modular_ec2.html')

#@app.route('/lib/<path:path>')
#def send_foo(path):
#    return send_from_directory('lib', path)

@app.route("/api/points")
def hello_combined(brand, gram):
    rdict = { 'text': text, 'size': size}
    r = Response(json.dumps(rdict), mimetype='application/json')
    r.headers["Access-Control-Allow-Origin"] = '*'
    return r

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
