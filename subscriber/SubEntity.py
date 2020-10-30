import paho.mqtt.client as mqtt
import time
import threading

class SubEntity:
    def __init__(self):
        broker_address="localhost" 
        client = mqtt.Client("SubEntity")
        clientP = mqtt.Client("SubEntity2")
        
        client.connect(broker_address)
        clientP.connect(broker_address)
        
        client.on_message=self.on_message
        clientP.on_message=self.on_message
        
        myt =  threading.Thread(target=self.infinite_listen, args=("ch1", client,))
        mytP =  threading.Thread(target=self.infinite_listen, args=("ch2", clientP,))
        
        myt.start()
        mytP.start()
        
    def infinite_listen(self, topic, client):
        print(topic)
        print(client)
        while True:
            client.loop_start()
            client.subscribe(topic)
            time.sleep(2)
        
    def on_message(self, client, userdata, message):
        print("message received " ,str(message.payload.decode("utf-8")))
        print("message topic=",message.topic)
        print("message qos=",message.qos)
        print("message retain flag=",message.retain)
        