from dotenv import load_dotenv
load_dotenv()
import os
MQTT_SERVER = os.getenv("MQTT_SERVER")
MQTT_SERVER_PORT  = os.getenv("MQTT_SERVER_PORT")
MQTT_USER = os.getenv('MQTT_USER')
MQTT_PASS = os.getenv('MQTT_PASS')
BLYNK_SERVER = os.getenv('BLYNK_SERVER')
BLYNK_SERVER_PORT = os.getenv('BLYNK_SERVER_PORT')
import threading
from utils import on_connect, on_message, start_blynk_client_threads
import paho.mqtt.client as mqtt

# ! Send Last time of device to vpin 10 and check time and put it as retained message to status and check the value and compare it to current time
# create the client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
# enable TLS
client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set(MQTT_USER, MQTT_PASS)
# connect to HiveMQ Cloud on port 8883
client.connect(MQTT_SERVER,int(MQTT_SERVER_PORT))
client.subscribe("blynk/#")
#starting blynk client threads
start_blynk_client_threads(client=client)

t=threading.Thread(target=client.loop_forever)
t.start()
print("MQTT SERVER CONNECTED")
# client.loop_forever()
# print("Does it print ??/")