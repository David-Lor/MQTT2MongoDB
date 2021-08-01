# MQTT2MongoDB

A simple Python project that listen to one or more MQTT topics and save all the incoming messages on a MongoDB database, as some sort of logger.

## Requirements

- Python 3.x (tested on 3.9)
- Tested on Docker with docker-compose on Mac OS Big Sur
- A working, available MQTT broker
- A working, available MongoDB server
- Libraries:
    * [pymongo](https://pypi.org/project/pymongo/)
    * [paho-mqtt](https://pypi.org/project/paho-mqtt/)
- Docker + docker-compose is recommended if available

---

## Settings
Settings for MQTT Broker and MongoDB server can be placed on the ***"appsettings.json"*** file.

---

## Features
- [x] MQTT with callback and subscribers list of topics
- [x] MongoDB with new thread for each save in MongoDB
- [x] Queue implemented to communicate data between MQTT and MongoDB
- [x] Decode JSON from MQTT message and save as Object in MongoDB

---

## Format of a Mongo document
When payload is a text will be something like
```json
{
    "_id": {
        "$oid": "6106005077a6c6ab86883751"
    },
    "topic": "topic1/subtopic/test1",
    "payload": "message text test",
    "qos": 0,
    "timestamp": 1627783248,
    "datetime": "01/08/2021 02:00:48"
}
```
Or when your payload is a json, the document in mongodb will be like below
```json
{
    "_id":{"$oid":"6105f8d777a6c6ab86883750"},
    "topic":"topic1/subtopic/test1",
    "payload": {
        "var1":1.99,
        "var2":"variable2"
        },
    "qos":0,
    "timestamp":1627781335,
    "datetime":"01/08/2021 01:28:55"
}
```
---

## Debug with docker-compose 
To Debug with docker container and vscode use the command below
```bash
docker-compose -f "docker-compose.yml" -f "docker-compose.debug.yml" up --build -d
```
and use "Python: Remote Attach" configuration on vscode build option.

---

## Run as production
To run as service on background use the command below
```bash
docker-compose -f "docker-compose.yml" up --build -d
```

