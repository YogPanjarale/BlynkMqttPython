import time
import blynklib as BlynkLib
from paho.mqtt.client import Client, MQTTMessage

from threading import Thread
pins_to_watch = [11, 12, 13]


class BlynkClientThread(Thread):
    PING_PIN = 0
    def __init__(self, token: str, mqtt_client: Client, server="yog1.ddns.net", port=8080):
        super(BlynkClientThread, self).__init__()
        self.token = token
        self.mqtt_client = mqtt_client
        self.blynk = BlynkLib.Blynk(token, server=server, port=port)
        print(
            f"Blynk Client Thread started for token: {token} , server: {server}, port: {port}")
        self.blynk.connect()
        self.last_online
        # mqtt callbacks
        self.mqtt_client.message_callback_add(
            f"blynk/{self.token}/#", self.mqtt_callback)
        # write callbacks
        def w(*args):
            print(*args)
            self.blynk_write_event(args[0], args[1][0])
        self.blynk.handle_event("write v*")(func=w)

    def mqtt_callback(self, client: Client, userdata, msg: MQTTMessage):
        # print(f"Msg recived at {msg.topic} -> {msg.payload.decode('utf-8')}")
        def mqtt_write_event(self, topic: str, value: str):
            try:
                pin = topic.split("/")[-1].removeprefix("V")
                # print("pin: ",pin)
                self.blynk.virtual_write(pin, value)
                # print(f"Publishing to Blynk {self.token} on V{pin} -> {value}")
            except:
                pass
        mqtt_write_event(topic=msg.topic, value=msg.payload.decode('utf-8'))

    def blynk_write_event(self, pin: int, value: str):
        if pin == self.PING_PIN and str(value) == '1':
            print(".", end='')
            self.update_last_online()
        self.mqtt_client.publish(
            topic=f"blynk/{self.token}/V{pin}", payload=str(value))
        # print(f"Publising to blynk/{self.token}/V{pin}  -> {value}")

    def update_last_online(self):
        update_topic = f'blynk/{self.token}/last_online'
        self.last_online=time.time()
        self.mqtt_client.publish(update_topic,self.last_online)

    def run(self):
        while True:
            self.blynk.run()

