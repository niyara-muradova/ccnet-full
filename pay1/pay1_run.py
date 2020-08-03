import time
import requests

import redis

while True:
    try:
        conn = redis.StrictRedis(decode_responses=True)
        result = conn.get('payment:result')
    except:
        print("try next connect to redis after 30sec..")
        time.sleep(30)
        continue
    else:
        break
 
result = conn.get('payment:result')

if result == None:

    conn.set('payment:result', 1)
    conn.set('payment:msg', '')
    conn.set('payment:success', '')

print('main loop started.')

count = 0

while True:

    result = conn.get('payment:result')
    msg = conn.get('payment:msg')
    success = conn.get('payment:success')


    if result == '1':

        if conn.llen('payment:in') > 0:
            conn.set('payment:result', 0)
            conn.set('payment:msg', conn.lpop('payment:in'))
            count = 0

    if result == '0':

        if msg != success:

            try:
                url = 'https://terminal.indigo24.xyz/api/v2/kafka/payments/in'
                payload = {"_token": '!#j_Y@Q9pDg84', "data": "{}".format(msg)}
                headers = {"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"}

                x = requests.post(url, data=payload, headers=headers)
                status = x.text

            except:
                #pass
                print('Error connect or send msg to backend server. Try next send message after 2 sec..')

            else:
                
                if status.strip() == "00":
                    conn.set('payment:result', 1)
                    conn.set('payment:success', msg)

                    conn.rpush('payment:ok', msg)

                    print('send message -> {}'.format(msg))
                else:
                    count+=1
                    print('error status {} count:{} -> {}'.format(status, count, msg))

                    if count>10:
                        conn.set('payment:result', 1)
                        conn.set('payment:msg', '')
                        conn.set('payment:success', '')

                        conn.rpush('payment:denial', msg)

                        print('denial of service -> {}'.format(msg))
                        

            finally:
                pass



    time.sleep(2)
    continue

