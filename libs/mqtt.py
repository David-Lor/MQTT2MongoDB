from json.decoder import JSONDecodeError
from typing import Dict
from datetime import datetime
from queue import Queue
import paho.mqtt.client as mqtt
import json

# MQTT_BROKER = "127.0.0.1"
# MQTT_PORT = 1883
# MQTT_KEEPALIVE = 60
# MQTT_QOS = 2
# MQTT_TOPICS = ("#",)  # Array of topics to subscribe; '#' subscribe to ALL available topics

# MQTT_BROKER = os.getenv("MQTT_BROKER", MQTT_BROKER)
# MQTT_PORT = os.getenv("MQTT_PORT", MQTT_PORT)
# MQTT_KEEPALIVE = os.getenv("MQTT_KEEPALIVE", MQTT_KEEPALIVE)
# MQTT_QOS = os.getenv("MQTT_QOS", MQTT_QOS)
# MQTT_TOPICS = os.getenv("MQTT_TOPICS", MQTT_TOPICS)  # As ENV, comma separated
# if isinstance(MQTT_TOPICS, str):
#     MQTT_TOPICS = [e.strip() for e in MQTT_TOPICS.split(",")]


class MQTT(object):
    def __init__(self, mqttConfig:dict, queue:Queue):
        self.__set_vars(mqttConfig)
        self.queue: Queue = queue
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message

    def __set_vars(self, config:dict):
        self.MQTT_BROKER = config["HOST"]
        self.MQTT_PORT = config["PORT"]
        self.MQTT_KEEPALIVE = config["KEEPALIVE"]
        self.MQTT_QOS = config["QOS"]
        self.MQTT_TOPICS = config["TOPICS"]
        self.MQTT_DATETIME_FORMAT = "%d/%m/%Y %H:%M:%S"

    # noinspection PyUnusedLocal
    # @staticmethod
    def on_connect(self, client: mqtt.Client, userdata, flags, rc):
        print("Connected MQTT")
        print("Connected with result code "+str(rc))
        for topic in self.MQTT_TOPICS:
            client.subscribe(topic, self.MQTT_QOS)

    # noinspection PyUnusedLocal
    def on_message(self, client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
        data = self.__createMsg(msg)
        print(f"Rx MQTT | msg: {data}")
        if not msg.retain:
            self.queue.put(data)

    def run(self):
        print(f"Running MQTT | BROKER: {self.MQTT_BROKER} PORT:{self.MQTT_PORT}")
        self.mqtt_client.connect(
            host=self.MQTT_BROKER,
            port=self.MQTT_PORT,
            keepalive=self.MQTT_KEEPALIVE)
        self.mqtt_client.loop_start()

    def stop(self):
        print("Stopping MQTT")
        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()

    def __createMsg(self, msg: mqtt.MQTTMessage) -> dict:
        return dict({
            "topic": msg.topic,
            "payload": self.__checkJsonInPayload(msg.payload),
            # "retained": msg.retain,
            "qos": msg.qos,
            "timestamp": int(datetime.now().timestamp()),
            "datetime": datetime.now().strftime(self.MQTT_DATETIME_FORMAT),
        })
    
    def __checkJsonInPayload(self, payload:bytes):
        data = payload.decode(encoding="utf-8")
        try:
            return json.loads(data)
        except JSONDecodeError:
            return data
