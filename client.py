"""
TODO:
    - Add device MISSING add listener for actuators, alarm and camera
    - Communication device/broker 
    - Communication broker/client MISSING lookup in db
    - Configuration of the server ????? 
    - Backup of the server 
    -Connection to db DONE  
    -DB CRUD DONE 
"""
import os
import paho.mqtt.client as mqtt
# Publish messages to a channel
broker_address="192.168.1.92" 
client=mqtt.Client("pepe")
client.connect(broker_address)
client.publish("x/spooky","Im sad")
