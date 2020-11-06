import uuid
from data.Database import Database
from datetime import datetime
from utils.constants import Devices
from utils.parsers import get_device_type, mqtt_to_string, get_tokens_from_client
from subscriber.SubEntity import SubEntity
from publisher.PubEntity import PubEntity

from utils.constants import SERVER_IP, SERVER_PORT, SERVER_USER, SERVER_PASSWORD, NEW_DEVICES_SUBSCRIBER_NAME, NEW_DEVICES_TOPIC, CLIENT_SUBSCRIBER_NAME


def insert_new_device(client, userdata, message):
    device_name = str(message.payload.decode("utf-8"))
    current_time = datetime.now().strftime("%H:%M:%S")

    database_connection = Database()
    database_connection.insert_into(Database.dispositivo_table, [(device_name, current_time)])
    
    device_type = get_device_type(device_name)
    device_id = database_connection.get_from("ID", Database.dispositivo_table, "Direccion", device_name)[0][0]
    
    actuador_id = ""
    if device_type in (Devices.Other, Devices.Camara, Devices.Alarma):
        print("1")
        database_connection.insert_into(Database.actuador_table, [(0, device_id)])
        actuador_id = database_connection.get_from("ID", Database.actuador_table, "Dispositivo_ID", device_id)[0][0]
        
    subscribrer_id = str(uuid.uuid1())
    if device_type == Devices.Sensor:
        print("2")
        database_connection.insert_into(Database.sensor_table, [(0.0, device_id)])
        device_sub = SubEntity(subscribrer_id, SERVER_IP, SERVER_PORT, SERVER_USER, SERVER_PASSWORD)
        device_sub.connect_and_subscribe_to_topic(device_name , listen_and_insert)
    elif device_type == Devices.Camara:
        print("3")
        database_connection.insert_into(Database.camara_table, [("RutaArchivoCamara", actuador_id)])
    elif device_type == Devices.Alarma:
        print("4")
        database_connection.insert_into(Database.alarma_table, [("MensajeAlarma", actuador_id)])
    


def listen_and_insert(client, userdata, message):
    received_value = mqtt_to_string(message)
    subscribed_topic = message.topic
    database_connection = Database()
    device_id = database_connection.get_from("ID", Database.dispositivo_table, "Direccion", subscribed_topic)[0][0]
    database_connection.update_row(Database.sensor_table, Database.sensores_foreign_key ,device_id,[float(received_value),None])
    
def listen_client(client, userdata, message):
    print("here1")
    (method, topic, parameters) = get_tokens_from_client(mqtt_to_string(message))
    print("here2")
    print(f"{method} {topic} {parameters}")
    if method == "get":
        #Search into the database
        pass
    else:
        pub = PubEntity(CLIENT_SUBSCRIBER_NAME, SERVER_IP, SERVER_PORT, SERVER_USER, SERVER_PASSWORD)
        pub.connect_and_publish_to_topic(topic, parameters)
        

def my_on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)   