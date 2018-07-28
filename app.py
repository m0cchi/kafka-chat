from bottle import route, run, static_file
from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket
import threading
from kafka import KafkaConsumer, KafkaProducer
import redis

users = set()

producer = KafkaProducer(bootstrap_servers='kafka1:9092')
msg_consumer = KafkaConsumer('chat', bootstrap_servers='kafka2:9092')
img_consumer = KafkaConsumer('image', bootstrap_servers='kafka2:9092')
pool = redis.ConnectionPool(host='kafka-chat-cache', port=6379, db=0)
redis_c = redis.StrictRedis(connection_pool=pool)

def send_all_message(user):
    for msg in redis_c.lrange('chat', 0, 100):
        user.send(msg.decode('utf-8'))

def send_message():
    for msg in msg_consumer:
        text = msg.value.decode('utf-8')
        for u in users:
            u.send(text)
        redis_c.rpush('chat', text)
threading.Thread(target=send_message).start()

def send_image():
    for msg in img_consumer:
        producer.send('chat', msg.value)
            
threading.Thread(target=send_image).start()

@route('/')
def index():
    return static_file('index.html', root='./statics')

@route('/statics/<filename:re:.*>')
def statics(filename):
    return static_file(filename, root='./statics')

@route('/chat', apply=[websocket])
def chat(ws):
    users.add(ws)
    send_all_message(ws)
    while True:
        msg = ws.receive()
        if msg is not None:
            producer.send('chat', msg.encode('utf-8')) #.get(timeout=1)            
        else:
            break
    users.remove(ws) # これ、thread-safeじゃないよね...

run(host='0.0.0.0', port=8080, debug=True, server=GeventWebSocketServer)
