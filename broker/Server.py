import subprocess
import os 
import psutil

class Server: 
    def __init__(self, ip="localhost", port="1883", new_device_topic="/SAM/nuevosDispositivos"):
        self.port = port
        self.ip = ip 
        self.default_topic = new_device_topic
        self.__start_server()
    
    def __start_server(self):
        sudoPassword = '1234'
        command = 'systemctl enable mosquitto'
        # A successful command returns a 0
        mosquito_enable_result = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
        mosquito_running = "mosquitto" in (process.name() for process in psutil.process_iter())

        if mosquito_enable_result or not mosquito_running:
            print("Server cannot be started")
        else:
            print("Server running")