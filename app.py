from bottle import route, run, static_file, get
from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket
import threading
from kafka import KafkaConsumer, KafkaProducer

users = set()

producer = KafkaProducer(bootstrap_servers='kafka1:9092')
msg_consumer = KafkaConsumer('chat', bootstrap_servers='kafka2:9092')
img_consumer = KafkaConsumer('image', bootstrap_servers='kafka2:9092')

def receive_messages():
    for msg in msg_consumer:
        for u in users:
            u.send(msg.value.decode('utf-8'))
threading.Thread(target=receive_messages).start()

def receive_image():
    for msg in img_consumer:
        for u in users:
            u.send(msg.value.decode('utf-8'))
threading.Thread(target=receive_image).start()

@route('/')
def index():
    return static_file('index.html', root='./statics')

@route('/statics/<filename:re:.*>')
def statics(filename):
    return static_file(filename, root='./statics')

@get('/chat', apply=[websocket])
def chat(ws):
    users.add(ws)
    while True:
        msg = ws.receive()
        if msg is not None:
            producer.send('chat', msg.encode('utf-8')) #.get(timeout=1)
        else:
            break
    users.remove(ws) # これ、thread-safeじゃないよね...

run(host='0.0.0.0', port=8080, debug=True, server=GeventWebSocketServer)
