import paho.mqtt.client as mqtt
import time
import threading

from utils.ThreadManager import ThreadManager


class SubEntity:
    def __init__(self, entity_name, broker_ip, port, user, password):
        self.entity_name = entity_name 
        self.broker_ip = broker_ip
        self.port = port
        self.user = user
        self.password = password
        self.client = None 
    
    def __connect(self, on_message_function):
        self.client = mqtt.Client(self.entity_name)
        self.client.connect(self.broker_ip)
        self.client.on_message= on_message_function 

    def __subscribe(self):
        return ThreadManager.create_new_thread(self.__infinite_listen, (self.client, self.topic,))
        
    def __infinite_listen(self, client, topic):
        while True:
            client.loop_start()
            client.subscribe(topic)
            time.sleep(0.1)

    def connect_and_subscribe_to_topic(self, topic, on_message_function):
        self.topic = topic
        self.__connect(on_message_function)
        subscriber_thread = self.__subscribe()
        ThreadManager.start_thread(subscriber_thread)
        