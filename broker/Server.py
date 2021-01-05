import subprocess
import os 
import psutil
import uuid
from data.Database import Database
from utils.constants import Devices
from utils.on_messages import general_listen_and_insert
from utils.parsers import get_device_type
from subscriber.SubEntity import SubEntity
from utils.constants import SUDO_PASSWORD, SERVER_IP, SERVER_PORT, SERVER_USER, SERVER_PASSWORD, NEW_DEVICES_SUBSCRIBER_NAME, NEW_DEVICES_TOPIC, CLIENT_SUBSCRIBER_NAME, CLIENT_TOPIC

class Server: 
    def __init__(self, ip="localhost", port="1883", new_device_topic="/SAM/nuevosDispositivos"):
        self.port = port
        self.ip = ip 
        self.default_topic = new_device_topic
        self.__start_server()
        self.__recover_mosquitto_topics()
    
    def __start_server(self):
        command = 'systemctl enable mosquitto'
        # A successful command returns a 0
        mosquito_enable_result = os.system('echo %s|sudo -S %s' % (SUDO_PASSWORD, command))
        mosquito_running = "mosquitto" in (process.name() for process in psutil.process_iter())

        if mosquito_enable_result or not mosquito_running:
            print("Server cannot be started")
        else:
            print("Server running")
            
    def __recover_mosquitto_topics(self):
        print(f"Recoverying previous topics")
        
        # Query the database and get all the channels
        database_connection = Database()
        all_topics = database_connection.get_all_topics()
        
        # From channels get the type of the device
        # Create a subentity with the specific on message required by the type
        for topic in all_topics:
            topic = topic[0]
            subscribrer_id = str(uuid.uuid1())
            device_sub = SubEntity(subscribrer_id, SERVER_IP, SERVER_PORT, SERVER_USER, SERVER_PASSWORD)
            device_sub.connect_and_subscribe_to_topic(topic, general_listen_and_insert)

            """
            device_type = get_device_type(topic)
            subscribrer_id = str(uuid.uuid1())
            if device_type == Devices.Sensor:
                device_sub = SubEntity(subscribrer_id, SERVER_IP, SERVER_PORT, SERVER_USER, SERVER_PASSWORD)
                device_sub.connect_and_subscribe_to_topic(topic, listen_and_insert_values_from_sensor)
            elif device_type == Devices.Camara:
                camera_sub = SubEntity(subscribrer_id, SERVER_IP, SERVER_PORT, SERVER_USER, SERVER_PASSWORD)
                camera_sub.connect_and_subscribe_to_topic(topic, listen_and_insert_ip_from_camera)
            """
         