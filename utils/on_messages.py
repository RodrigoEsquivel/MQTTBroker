from data.Database import Database
from datetime import datetime
from utils.constants import Devices
from utils.parsers import get_device_type

def insert_new_device(client, userdata, message):
    device = str(message.payload.decode("utf-8"))
    current_time = datetime.now().strftime("%H:%M:%S")
    
    database_connection = Database()
    database_connection.insert_into(Database.dispositivo_table, [(device, current_time)])
    
    device_type = get_device_type(device)
    device_id = database_connection.get_from("ID", Database.dispositivo_table, "Direccion", device)[0][0]
    
    actuador_id = ""
    if device_type in (Devices.Other, Devices.Camara, Devices.Alarma):
        print("1")
        database_connection.insert_into(Database.actuador_table, [(0, device_id)])
        actuador_id = database_connection.get_from("ID", Database.actuador_table, "Dispositivo_ID", device_id)[0][0]
        
    if device_type == Devices.Sensor:
        print("2")
        database_connection.insert_into(Database.sensor_table, [(0.0, device_id)])
    elif device_type == Devices.Camara:
        print("3")
        database_connection.insert_into(Database.camara_table, [("RutaArchivoCamara", actuador_id)])
    elif device_type == Devices.Alarma:
        print("4")
        database_connection.insert_into(Database.alarma_table, [("MensajeAlarma", actuador_id)])

def my_on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)   