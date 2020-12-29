import uuid
from data.Database import Database
from datetime import datetime
from utils.constants import Devices
from utils.parsers import get_device_type, mqtt_to_string, get_tokens_from_client, is_client
from subscriber.SubEntity import SubEntity
from publisher.PubEntity import PubEntity


from utils.constants import SERVER_IP, SERVER_PORT, SERVER_USER, SERVER_PASSWORD, NEW_DEVICES_SUBSCRIBER_NAME, NEW_DEVICES_TOPIC, CLIENT_SUBSCRIBER_NAME, CLIENT_TOPIC, DELETE_DEVICES_TOPIC, DELETE_DEVICES_SUBSCRIBER_NAME

def insert_new_device(client, userdata, message):
    device_name = mqtt_to_string(message)
    current_time = datetime.now().strftime("%H:%M:%S")

    database_connection = Database()
    database_connection.insert_into(Database.dispositivo_table, [(device_name, current_time)])
    
    device_type = get_device_type(device_name)
    device_id = database_connection.get_from("ID", Database.dispositivo_table, "Direccion", device_name)[0][0]

    actuador_id = ""
    # Puerta y Apagadores, solamente es push.
    if device_type in (Devices.Other, Devices.Camara, Devices.Alarma):
        print("1")
        database_connection.insert_into(Database.actuador_table, [(0, device_id)])
        actuador_id = database_connection.get_from("ID", Database.actuador_table, "Dispositivo_ID", device_id)[0][0]
        
    subscribrer_id = str(uuid.uuid1())
    if device_type == Devices.Sensor:
        print("2")
        database_connection.insert_into(Database.sensor_table, [(0.0, device_id)])
        #device_sub = SubEntity(subscribrer_id, SERVER_IP, SERVER_PORT, SERVER_USER, SERVER_PASSWORD)
        #device_sub.connect_and_subscribe_to_topic(device_name , listen_and_insert_values_from_sensor)
    elif device_type == Devices.Camara: 
        print("3")
        database_connection.insert_into(Database.camara_table, [("RutaArchivoCamara", actuador_id)])
        #camera_sub = SubEntity(subscribrer_id, SERVER_IP, SERVER_PORT, SERVER_USER, SERVER_PASSWORD)
        #camera_sub.connect_and_subscribe_to_topic(device_name, listen_and_insert_ip_from_camera)
        
    elif device_type == Devices.Alarma:
        print("4") #nosotros no nos subscribimos  a nada
        #nosotros publicamos a la alarma el mensaje que recibamos del cliente
        database_connection.insert_into(Database.alarma_table, [("MensajeAlarma", actuador_id)])
    
    general_sub = SubEntity(subscribrer_id, SERVER_IP, SERVER_PORT, SERVER_USER, SERVER_PASSWORD)
    general_sub.connect_and_subscribe_to_topic(device_name, general_listen_and_insert)

    # All topics when new device
    publish_all_devices()
     

def general_listen_and_insert(client, userdata, message):
    received_value = mqtt_to_string(message)
    subscribed_topic = message.topic
    device_type = get_device_type(subscribed_topic)
    database_connection = Database()
    device_id = database_connection.get_from("ID", Database.dispositivo_table, "Direccion", subscribed_topic)[0][0]
    if device_type == Devices.Sensor:
        print("U Sensor")
        database_connection.update_sensor_table_using(device_id, received_value)
    elif device_type == Devices.Camara: 
        print("U Camara")
        actuador_id = database_connection.get_from("ID", Database.actuador_table, "Dispositivo_ID", device_id)[0][0]
        database_connection.update_row(Database.camara_table, Database.camara_foreign_key ,actuador_id,[received_value,None])
    elif device_type == Devices.Alarma:
        print("U Alarma")
        actuador_id = database_connection.get_from("ID", Database.actuador_table, "Dispositivo_ID", device_id)[0][0]
        database_connection.update_alarma_table_using(actuador_id,received_value)
    elif device_type == Devices.Other:
        print("U Other")
        database_connection.update_actuadores_using(device_id, received_value)

""" 
def listen_and_insert_values_from_sensor(client, userdata, message):
    received_value = mqtt_to_string(message)
    subscribed_topic = message.topic
    database_connection = Database()
    device_id = database_connection.get_from("ID", Database.dispositivo_table, "Direccion", subscribed_topic)[0][0] # get_device_id_from_dispositivo_with_topic
    database_connection.update_row(Database.sensor_table, Database.sensores_foreign_key ,device_id,[float(received_value),None])

def listen_and_insert_ip_from_camera(client, userdata, message):
    camera_ip = mqtt_to_string(message)
    subscribed_topic = message.topic
    database_connection = Database()
    device_id = database_connection.get_from("ID", Database.dispositivo_table, "Direccion", subscribed_topic)[0][0] # get_id_from_dispositivo_with_topic
    actuador_id = database_connection.get_from("ID", Database.actuador_table, "Dispositivo_ID", device_id)[0][0]
    database_connection.update_row(Database.camara_table, Database.camara_foreign_key ,actuador_id,[camera_ip,None])
"""
def delete_device(client, userdata, message):
    received_value = mqtt_to_string(message)
    device_type = get_device_type(received_value)
    database_connection = Database()
    device_id = database_connection.get_from("ID", Database.dispositivo_table, "Direccion", received_value)[0][0]
    print(device_id)
    if device_type == Devices.Sensor:
        print("D Sensor")
        sensor_id = database_connection.get_id_from_sensores_with_device_id(device_id)
        print(sensor_id)
        database_connection.delete_from_single(Database.sensor_table,sensor_id)
        database_connection.delete_from_single(Database.dispositivo_table,device_id)
    elif device_type == Devices.Camara: 
        print("D Camara")
        actuador_id = database_connection.get_from("ID", Database.actuador_table, "Dispositivo_ID", device_id)[0][0]
        camara_id = database_connection.get_id_from_camara_with_actuador_id(actuador_id)
        database_connection.delete_from_single(Database.camara_table,camara_id)
        database_connection.delete_from_single(Database.actuador_table,actuador_id)
        database_connection.delete_from_single(Database.dispositivo_table,device_id)
    elif device_type == Devices.Alarma:
        print("D Alarma")
        actuador_id = database_connection.get_from("ID", Database.actuador_table, "Dispositivo_ID", device_id)[0][0]
        alarma_id = database_connection.get_id_from_alarma_with_actuador_id(actuador_id)
        database_connection.delete_from_single(Database.alarma_table,alarma_id)
        database_connection.delete_from_single(Database.actuador_table,actuador_id)
        database_connection.delete_from_single(Database.dispositivo_table,device_id)
    elif device_type == Devices.Other:
        print("D Other")
        actuador_id = database_connection.get_from("ID", Database.actuador_table, "Dispositivo_ID", device_id)[0][0]
        database_connection.delete_from_single(Database.actuador_table,actuador_id)
        database_connection.delete_from_single(Database.dispositivo_table,device_id)
    publish_all_devices()

def listen_client(client, userdata, message):
    if is_client(mqtt_to_string(message)):
        print("*******")
        new_devices_sub = SubEntity(NEW_DEVICES_SUBSCRIBER_NAME, SERVER_IP, SERVER_PORT, SERVER_USER, SERVER_PASSWORD)
        new_devices_sub.connect_and_subscribe_to_topic(NEW_DEVICES_TOPIC , insert_new_device)    
        delete_devices_sub = SubEntity(DELETE_DEVICES_SUBSCRIBER_NAME, SERVER_IP, SERVER_PORT, SERVER_USER, SERVER_PASSWORD)
        delete_devices_sub.connect_and_subscribe_to_topic(DELETE_DEVICES_TOPIC , delete_device)
    """
    (method, topic, parameters) = get_tokens_from_client(mqtt_to_string(message))
    device_type = get_device_type(topic)
    database_connection = Database()

    if method == "get":
        if device_type in (Devices.Sensor, Devices.Camara):
            device_id = database_connection.get_id_from_dispositivo_with_topic(topic)
            valor = None 
            if device_type == Devices.Sensor:
                valor = database_connection.get_valor_from_sensores_with_device_id(device_id)
            elif device_type == Devices.Camara:
                actuador_id = database_connection.get_id_from_actuador_with_device_id(device_id)
                valor = database_connection.get_archivo_from_camara_with_actuador_id(actuador_id)
            pub = PubEntity(CLIENT_SUBSCRIBER_NAME, SERVER_IP, SERVER_PORT, SERVER_USER, SERVER_PASSWORD)
            print(f"ENTERED HERE {topic} {valor}")
            pub.connect_and_publish_to_topic(CLIENT_TOPIC, f"{topic} {valor}")
    elif method == "set":
        if device_type not in (Devices.Sensor, Devices.Camara):
            # TODO: Validate non integer values
            if device_type == Devices.Other:
                device_id = database_connection.get_id_from_dispositivo_with_topic(topic)
                database_connection.update_actuadores_with(device_id, parameters)
            elif device_type == Devices.Alarma:
                device_id = database_connection.get_id_from_dispositivo_with_topic(topic)
                actuador_id = database_connection.get_id_from_actuador_with_device_id(device_id)
                database_connection.update_alarma_table_using(actuador_id, parameters)
            pub = PubEntity(CLIENT_SUBSCRIBER_NAME, SERVER_IP, SERVER_PORT, SERVER_USER, SERVER_PASSWORD)
            pub.connect_and_publish_to_topic(topic, parameters)
    """
#This is not an on message method
def publish_all_devices():
    database_connection = Database()
    all_topics = database_connection.get_all_topics()
    formatted_topics = ','.join([str(elem[0]) for elem in all_topics])
    pub = PubEntity(CLIENT_SUBSCRIBER_NAME, SERVER_IP, SERVER_PORT, SERVER_USER, SERVER_PASSWORD)
    pub.connect_and_publish_to_topic(CLIENT_TOPIC, formatted_topics)