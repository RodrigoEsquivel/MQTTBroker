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