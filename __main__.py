import queue
from libs.mongo import Mongo
from libs.mqtt import MQTT
from libs.configuration import Configuration

from queue import Queue
from signal import pause
import threading




if __name__ == "__main__":
    configuration = Configuration()
    __queue = Queue()
    mongo = Mongo(
        mongoConfig = configuration.AppConfiguration["MONGODB"],
        queue = __queue)
    mqtt = MQTT(
        mqttConfig = configuration.AppConfiguration["MQTT"],
        queue = __queue)

    mongo.connect()
    mqtt.run()

    th = []
    th.append( threading.Thread(target=mongo.run,) )
    th.append( threading.Thread(target=mqtt.run,) )

    for t in th:
        t.daemon = True
        t.start()
    try:
        pause()
    except KeyboardInterrupt:
        pass

    # mqtt.stop()
    # mongo.disconnect()
