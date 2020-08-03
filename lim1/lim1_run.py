import json
import time

import string
import random

import requests

import redis

from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/limit/load', methods=['POST']) 
def limit_load():

    data = request.get_data()
    msg = json.loads(data)

    url = "http://localhost:5000/credit/load"  
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url, data=json.dumps(msg), headers=headers)
    
    data = json.dumps(r.json(), separators=(",", ":"))
    #send response
    res = app.make_response(data)
    res.headers['Access-Control-Allow-Origin'] = '*'

    return res

@app.route('/limit/free', methods=['GET']) 
def limit_free():
    c=requests.get(url = 'http://localhost:5000/credit/info')
    limit = c.json()

    free_token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))
    msg = {'token': free_token, 'credit': limit['credit']}

    data = json.dumps(msg, separators=(",", ":"))

    r.set("credit:token", data)

    #send response
    res = app.make_response(data)
    res.headers['Access-Control-Allow-Origin'] = '*'

    return res


@app.route('/limit/info', methods=['GET']) 
def limit_info():
    c=requests.get(url = 'http://localhost:5000/credit/info')
    #send response
    data = json.dumps(c.json(), separators=(",", ":"))     
    res = app.make_response(data)
    res.headers['Access-Control-Allow-Origin'] = '*'

    return res

r = redis.StrictRedis(host="localhost", port=6379, password="", decode_responses=True)
app.run(host='10.10.1.126', port=50001)

