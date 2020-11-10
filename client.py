"""
TODO:
    - Add device DONE 
    - Communication broker/client MISSING GET 
    - Configuration of the server ????? 
    - Backup of the server MISSING restore mqtt channels from database
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
