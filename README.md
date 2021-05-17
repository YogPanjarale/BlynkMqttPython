# Mqtt-Blynk Bridge

## Instructions

1. make `.env` file with such content

```bash
MQTT_SERVER=yourserverdomain
MQTT_SERVER_PORT = port of mqtt
MQTT_USER = yourusername
MQTT_PASS = youruserpassword
BLYNK_SERVER = blynk-cloud.com
BLYNK_SERVER_PORT = 80
```

2. Make `tokens.txt` file with list of all tokens you want to bridge
example

```txt
token1knjnjnjbj
token2kdasascad
```

3. run `pip install -r requirements.txt`

4. run main.py

