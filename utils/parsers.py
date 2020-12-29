import re
from utils.constants import Devices 

def get_device_type(string):
    """
    Types of devices: 
   

       #gb
    /ST/T612  2 Sensor
    /SP/Y481  2 Sensor  
    /SL/3781  2
    /AP/4712  1 Other
    /AE/ASDA  1 Sensor
    /AA/RTYU  4 Alarma
    /AC/JKTI  3 Camara  

    """
    tokens = string.split('/')
    (_, device_id, _) = tokens
    device_type = device_id[0]
    if device_type == 'A':
        special_device = device_id[1]
        if special_device == 'A':
            return Devices.Alarma
        elif special_device == 'C':
            return Devices.Camara
        else:
            return Devices.Other
    return Devices.Sensor

def is_client(message):
    return bool(re.match(r"^/Cliente/C[0-9][0-9]$",message)) 

def mqtt_to_string(mqtt_message):
    return str(mqtt_message.payload.decode("utf-8"))
    
def get_tokens_from_client(string):
    tokens = string.split(" ") # set /AP2/ off, get /ST1/
    if tokens[0] == "set":
        return ("set", tokens[1], tokens[2])
    return ("get", tokens[1], None)