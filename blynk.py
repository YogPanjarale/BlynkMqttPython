import blynklib as BlynkLib
from paho.mqtt.client import Client, MQTTMessage

from threading import Thread
pins_to_watch = [11, 12, 13]
class BlynkClientThread(Thread):
    def __init__(self, token: str, mqtt_client: Client, server="yog1.ddns.net", port=8080):
        super(BlynkClientThread, self).__init__()
        self.token = token
        self.mqtt_client = mqtt_client
        self.blynk = BlynkLib.Blynk(token, server=server, port=port)
        print(f"Blynk Client Thread started for token: {token} , server: {server}, port: {port}")
        self.blynk.connect()
        self.blynk.virtual_write_msg(0,"Hello World")
        #mqtt callbacks
        def mqtt_callback(client:Client,userdata,msg:MQTTMessage):
            print(f"Msg recived at {msg.topic} -> {msg.payload.decode('utf-8')}")
            self.mqtt_write_event(topic=msg.topic,value=msg.payload.decode('utf-8'))
        self.mqtt_client.message_callback_add(f"blynk/{self.token}/#",mqtt_callback)
        #write callbacks
        def w(*args):
            print(*args)
            self.blynk_write_event(args[0], args[1][0])
        self.blynk.handle_event("write v*")(func=w)
    def mqtt_write_event(self,topic:str,value:str):
        try:
            pin =topic.split("/")[-1].removeprefix("V")
            print("pin: ",pin)
            self.blynk.virtual_write(pin,value)
            print(f"Publishing to Blynk {self.token} on V{pin} -> {value}")
        except:
            pass
    def blynk_write_event(self, pin: int, value:str):
        self.mqtt_client.publish(
            topic=f"blynk/{self.token}/V{pin}", payload=str(value))
        print(f"Publising to blynk/{self.token}/V{pin}  -> {value}")
    def run(self):
        while True:
            self.blynk.run()


def handle_message(topic: str, payload: str):
    print("Handling -> {} : -> {}".format(topic, payload))
    if topic.startswith("blynk/"):
        # blynk = blynklib.Blynk(topic.split("/")[1])
        # @blynk.handle_event('read V11')
        def e():
            pass
