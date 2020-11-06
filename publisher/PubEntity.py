import paho.mqtt.client as mqtt

class PubEntity:
    def __init__(self, entity_name, broker_ip, port, user, password):
        self.entity_name = entity_name 
        self.broker_ip = broker_ip
        self.port = port
        self.user = user
        self.password = password
        self.client = None 
    
    def __connect(self):
        self.client = mqtt.Client(self.entity_name)
        self.client.connect(self.broker_ip)

    def connect_and_publish_to_topic(self, topic, value):
        self.__connect()
        self.client.publish(topic, value)
        