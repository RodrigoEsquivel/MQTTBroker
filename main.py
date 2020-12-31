"""
TODO:
    - Add device DONE 
    - Communication broker/client DONE (client needs to wait like a second between messages)
    - Configuration of the server ????? 
    - Backup of the server DONE
    -Connection to db DONE  
    -DB CRUD DONE 
    -REFACTOR HARDCODED QUERIES

    2
    -modify parser DONE
    -VERIFY CLIENT ID DONE
    -MODIFY NUEVOSDISPOSITIVOS TO SUBSCRIBE TO ALL TOPICS AND UPDATE ON MESSAGES DONE    
    -BorrarDispositivo Topic and logic DONE
    -Setup sending of topics in comunicacion DONE
    -setup retained messages DONE
"""

from broker.Server import Server
from subscriber.SubEntity import SubEntity
from utils.on_messages import insert_new_device, publish_all_devices, delete_device
from utils.constants import SERVER_IP, SERVER_PORT, SERVER_USER, SERVER_PASSWORD, NEW_DEVICES_SUBSCRIBER_NAME, NEW_DEVICES_TOPIC, CLIENT_SUBSCRIBER_NAME, CLIENT_TOPIC, DELETE_DEVICES_SUBSCRIBER_NAME, DELETE_DEVICES_TOPIC

main_server = Server()
#publish_all_devices()
#new_devices_sub = SubEntity(NEW_DEVICES_SUBSCRIBER_NAME, SERVER_IP, SERVER_PORT, SERVER_USER, SERVER_PASSWORD)
#new_devices_sub.connect_and_subscribe_to_topic(NEW_DEVICES_TOPIC , insert_new_device)

#client_sub = SubEntity(CLIENT_SUBSCRIBER_NAME, SERVER_IP, SERVER_PORT, SERVER_USER, SERVER_PASSWORD)
#client_sub.connect_and_subscribe_to_topic(CLIENT_TOPIC , listen_client)
new_devices_sub = SubEntity(NEW_DEVICES_SUBSCRIBER_NAME, SERVER_IP, SERVER_PORT, SERVER_USER, SERVER_PASSWORD)
new_devices_sub.connect_and_subscribe_to_topic(NEW_DEVICES_TOPIC , insert_new_device)    
delete_devices_sub = SubEntity(DELETE_DEVICES_SUBSCRIBER_NAME, SERVER_IP, SERVER_PORT, SERVER_USER, SERVER_PASSWORD)
delete_devices_sub.connect_and_subscribe_to_topic(DELETE_DEVICES_TOPIC , delete_device)