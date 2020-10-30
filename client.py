"""
TODO:
    - Add device
    - Communication device/broker
    - Communication broker/client
    - Configuration of the server ????? 
    - Backup of the server 
    -Connection to db
    -DB CRUD
"""
import os
import paho.mqtt.client as mqtt
# Publish messages to a channel
broker_address="192.168.1.92" 
client=mqtt.Client("pepe")
client.connect(broker_address)
client.publish("x/spooky","Im sad")
