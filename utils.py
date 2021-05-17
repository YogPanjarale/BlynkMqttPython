# The callback for when the client receives a CONNACK response from the server.
from paho.mqtt.client import Client
from blynk import BlynkClientThread
blynk_client_threads = []
def start_blynk_client_threads(client:Client):
    tokens = readlines("tokens.txt")
    for t in tokens:
        t=BlynkClientThread(token=t,mqtt_client=client)
        t.start()
        blynk_client_threads.append(t)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
    else:
        print("Connect returned result code: " + str(rc))

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # pass
    print("Received message: " + msg.topic + " -> " + msg.payload.decode("utf-8"))
list_of_str = [ "",""]
def readlines(filepath:str)->list_of_str:
    lines = [i.strip() for i in open(filepath).readlines()]
    print(len(lines)," Tokens Found")
    return lines
    