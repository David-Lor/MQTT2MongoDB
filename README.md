# MQTT2MongoDB

A simple Python project that listen to one or more MQTT topics and save all the incoming messages on a MongoDB database, as some sort of logger.

## Requirements

- Python 3.x (tested on 3.7)
- Linux (not tested on other OS)
- A running MQTT broker
- Libraries:
    * [pymongo](http://api.mongodb.com/python/current/)
    * [paho-mqtt](https://pypi.org/project/paho-mqtt/)
- Docker recommended if available - you can use my [Python Autoclonable App Docker](https://hub.docker.com/r/davidlor/python-autoclonable-app/)

## Settings

Settings for MQTT and MongoDB can be placed on the mqtt.py and mongo.py files respectively, on a top-level UPPERCASE variables.

Alternatively, environment variables with the same names as these UPPERCASE variables are fetched instead of these variables, when available. This can be useful when running the app from a Docker container.

## Queue

(TODO) When the MongoDB server is unavailable or the insert failed, messages are stored on a list and periodically try to be inserted on the MongoDB again.

## Format of a Mongo document

```json
{
    "_id": "5c82de0799ec3656ff38d215",
    "topic": "home/test",
    "payload": "This is a test!",
    "qos": 2,
    "timestamp": 1552080391,
    "datetime": "08/03/2019 22:26:31"
}
```
