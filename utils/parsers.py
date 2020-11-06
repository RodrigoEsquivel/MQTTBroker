from utils.constants import Devices 

def get_device_type(string):
    tokens = string.split('/')
    (_, project_name, device_id) = tokens
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
    
def mqtt_to_string(mqtt_message):
    return str(mqtt_message.payload.decode("utf-8"))
    
def get_tokens_from_client(string):
    tokens = string.split(" ") # set /AP2/ off, get /ST1/
    if tokens[0] == "set":
        return ("set", tokens[1], tokens[2])
    return ("get", tokens[1], None)