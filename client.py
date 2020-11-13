"""
TODO:
    - Add device DONE 
    - Communication broker/client DONE (client needs to wait like a second between messages)
    - Configuration of the server ????? 
    - Backup of the server DONE
    -Connection to db DONE  
    -DB CRUD DONE 
    -REFACTOR HARDCODED QUERIES
"""
import os
import paho.mqtt.client as mqtt
# Publish messages to a channel
broker_address="192.168.1.92" 
client=mqtt.Client("pepe")
client.connect(broker_address)
client.publish("x/spooky","Im sad")
