import time
import blynklib as BlynkLib
from paho.mqtt.client import Client, MQTTMessage
from blynktimer import Timer
from threading import Thread
pins_to_watch = [11, 12, 13]

# bt.Timer()
class BlynkClientThread(Thread):
    PING_PIN = 0
    BLYNK_TIMEOUT = 10#10 seconds
    def __init__(self, token: str, mqtt_client: Client, server="yog1.ddns.net", port=8080):
        super(BlynkClientThread, self).__init__()
        self.token = token
        self.mqtt_client = mqtt_client
        self.blynk = BlynkLib.Blynk(token, server=server, port=port)
        self.timer = Timer()
        self.last_online_update = time.time()-(self.BLYNK_TIMEOUT+1)
        print(
            f"Blynk Client Thread started for token: {token} , server: {server}, port: {port}")
        self.blynk.connect()
        # mqtt callbacks
        def mc(*args):
            self.mqtt_callback(*args)
        self.mqtt_client.message_callback_add(
            f"blynk/{self.token}/#", mc)
        self.last_online:int
        # write callbacks
        def w(*args):
            print(*args)
            self.blynk_write_event(args[0], args[1][0])
        self.blynk.handle_event("write v*")(func=w)
        #setting timers
        def t():
            self.check_online()
        self.timer.register(interval=5,run_once=False)(func=t)
    def check_online(self,pin=1):
        try :
            print("'",end="")
            # print(type(time.time()),type(self.last_online),type(self.BLYNK_TIMEOUT))
            if (time.time()-self.last_online)>self.BLYNK_TIMEOUT:
                print("offline")
                self.set_device_status("offline")
            else:
                self.set_device_status("online")
                # print((time.time())-(self.last_online))
        except:
            pass
    def mqtt_callback(self,client: Client, userdata, msg: MQTTMessage,*args):
        # print(f"Msg recived at {msg.topic} -> {msg.payload.decode('utf-8')}")
        def mqtt_write_event( topic: str, value: str):
            try:
                pin = topic.split("/")[-1] 
                if pin=='last_online':
                    self.last_online = int(value)
                    # self.update_last_online()
                print(f"[{pin}]<- {value}")
                if pin.removeprefix("V").isnumeric():
                    self.blynk.virtual_write(pin.removeprefix("V"), value)
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
        self.mqtt_client.publish(update_topic,self.last_online,retain=True)
    def set_device_status(self,status:str):
        self.mqtt_client.publish(f"blynk/{self.token}/status",status)
    def run(self):
        while True:
            self.blynk.run()
            self.timer.run()

