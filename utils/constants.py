from enum import Enum, auto

class Devices(Enum):
   Sensor = auto()
   # Actuador= 2 *
   Camara = auto()
   Alarma = auto()
   Other = auto()
   
SERVER_IP = "localhost"
SERVER_PORT = "1883"
SERVER_USER = "test"
SERVER_PASSWORD = "1234"
NEW_DEVICES_SUBSCRIBER_NAME = "cliente1"
NEW_DEVICES_TOPIC = "NuevosDispositivos"
CLIENT_SUBSCRIBER_NAME = "cliente2"
CLIENT_TOPIC = "Comunicacion"