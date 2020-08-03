import cctalk_coin
import time
import threading
import json

import redis

from flask import Flask

time.sleep(10)

pool = cctalk_coin.CCTalkCoinAcceptor()

start = threading.Event() 
start.clear()

app = Flask(__name__)

def run_app():
    app.run(host='localhost', port=5001) 

@app.route('/device/on', methods=['GET']) 
def device_on():
    global STATE
    global start
    global r
    start.set()
    STATE={"coins":[], "last_coin":0, "income":0}
    data = json.dumps(STATE, separators=(",", ":"))
    r.set("sca1:state", data)                    
    return data

@app.route('/device/continue', methods=['GET']) 
def device_continue():
    global STATE
    global start
    global r
    start.set()
    data=r.get("sca1:state")
    STATE=json.loads(data)
    return data

@app.route('/device/off', methods=['GET']) 
def device_off():
    global STATE
    global start
    global pool
    start.clear()
    time.sleep(0.2)
    pool.send(pool.DisableCoins, True)
    data = json.dumps(STATE, separators=(",", ":"))
    return data

@app.route('/device/info', methods=['GET']) 
def device_info():
    global STATE
    data = json.dumps(STATE, separators=(",", ":"))
    return data

@app.route('/device/collection', methods=['GET']) 
def device_collection():
    global COLLECTION
    data = json.dumps(COLLECTION, separators=(",", ":"))
    return data

@app.route('/device/collection/reset', methods=['GET']) 
def device_collection_reset():
    global COLLECTION
    global r
    data = json.dumps(COLLECTION, separators=(",", ":"))
    
    COLLECTION = {"5":0, "10":0, "20":0, "50":0, "100":0, "200":0}
    new = json.dumps(COLLECTION, separators=(",", ":"))
    r.set("sca1:collection", new)
    
    return data
    
r = redis.StrictRedis(host="localhost", port=6379, password="", decode_responses=True)

# get last collection
data = r.get("sca1:collection")
if data==None:
    COLLECTION = {"5":0, "10":0, "20":0, "50":0, "100":0, "200":0}
    new = json.dumps(COLLECTION, separators=(",", ":"))
    r.set("sca1:collection", new)
else:
    COLLECTION = json.loads(data)

print("sca1:collection -> ", COLLECTION)

# get last state
data = r.get("sca1:state")
if data==None:
    STATE={"coins":[], "income": 0}
else:
    STATE = json.loads(data)

print("sca1:state -> ", STATE)

api = threading.Thread(target=run_app)
api.start()

while True:
    
    start.wait()
    
    pool.readConfig('default.conf')
    pool.CLEAR()
    
    pool.send(pool.ResetDevice, True)

    pool.send(pool.SimplePoll, True)

    pool.send(pool.RequestManufacturerId, True)

    pool.send(pool.RequestProductCode, True)

    pool.send(pool.RequestSerialNumber, True)

    pool.send(pool.RequestSoftwareRevision, True)

    pool.send(pool.RequestOptionFlags, True)

    pool.send(pool.EnableCoins, True)

    pool.send(pool.NormalOperation, True)

    for i in range(16):
        id = i+1
        pool.DATA = [id]
        pool.send(pool.RequestCoinId, True)

    for i in range(16):
        id = i+1
        pool.DATA = [id]
        pool.send(pool.RequestSorterPaths, True)

    pool.send(pool.RequestInhibitStatus, True)

    pool.send(pool.RequestSorterOverrideStatus, True)

    pool.send(pool.RequestDefaultSorterPath, True)

    pool.send(pool.POLL, True)
    pool.last_poll = pool.reply
    pool.counter = pool.event_counter
    pool.accepted = []
    pool.income = 0
    while True:
        pool.send(pool.POLL, False)
        if pool.last_poll != pool.reply:
            if (pool.counter + 1) == pool.event_counter:
                coin = pool.coins[pool.coin1A]
                sort = pool.coin1B
                pool.accepted += [coin]
                pool.income += coin
                pool.counter = pool.event_counter
                
                k=str(coin)
                
                COLLECTION[k] += 1

                data = json.dumps(COLLECTION, separators=(",", ":"))
                r.set("sca1:collection", data)
                
                STATE['coins'] += [coin]
                STATE['last_coin'] = coin
                STATE['income'] += coin
                
                print(STATE)
                
                data = json.dumps(STATE, separators=(",", ":"))
                
                r.set("sca1:state", data)                    
                
            #print('Event {}: accepted coin nominal {} KZT sorted path {} added to {} income {}'.format(
            #    pool.event_counter, coin, sort, pool.accepted, pool.income))

        pool.last_poll = pool.reply
        
        if not start.isSet():
            break
    

 
