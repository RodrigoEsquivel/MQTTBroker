"""
TODO:
    - Add device DONE 
    - Communication broker/client MISSING GET 
    - Configuration of the server ????? 
    - Backup of the server MISSING restore mqtt channels from database
    -Connection to db DONE  
    -DB CRUD DONE 
    -REFACTOR HARDCODED QUERIES
"""

from broker.Server import Server
from subscriber.SubEntity import SubEntity
from utils.on_messages import insert_new_device, listen_client
from utils.constants import SERVER_IP, SERVER_PORT, SERVER_USER, SERVER_PASSWORD, NEW_DEVICES_SUBSCRIBER_NAME, NEW_DEVICES_TOPIC, CLIENT_SUBSCRIBER_NAME, CLIENT_TOPIC

main_server = Server()
new_devices_sub = SubEntity(NEW_DEVICES_SUBSCRIBER_NAME, SERVER_IP, SERVER_PORT, SERVER_USER, SERVER_PASSWORD)
new_devices_sub.connect_and_subscribe_to_topic(NEW_DEVICES_TOPIC , insert_new_device)

client_sub = SubEntity(CLIENT_SUBSCRIBER_NAME, SERVER_IP, SERVER_PORT, SERVER_USER, SERVER_PASSWORD)
client_sub.connect_and_subscribe_to_topic(CLIENT_TOPIC , listen_client)