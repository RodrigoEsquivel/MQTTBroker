from utils.constants import Devices 

def get_device_type(string):
    """
    Types of devices: 
    /SAM/STemperatura/ST1  2 Sensor
    /SAM/SPresencia/SP1    2
    /SAM/SLiquido/SL1      2
    /SAM/APuerta/AP1       1 Other 
    /SAM/AEncendido/AE1    1
    /SAM/AAlarma/AA1       4 Alarma
    /SAM/ACamara/AC1       3 Camara
    """
    tokens = string.split('/')
    # _, used to ignore the spaces before the first / 
    (_, project_name, device_name, device_id) = tokens
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