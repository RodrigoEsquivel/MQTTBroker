# testing commands
- add new device
    1. Add a new alarm: ```mosquitto_pub -h localhost -p 1883 -t "NuevosDispositivos" -m "/AA/H123" ```  you need to change the -m string to add differeent types of devices with this format <br>
    Types of devices: 
    /ST/T612  2 Sensor
    /SP/Y481  2 Sensor  
    /SL/3781  2
    /AP/4712  1 Other
    /AE/ASDA  1 Sensor
    /AA/RTYU  4 Alarma
    /AC/JKTI  3 Camara 




- get value as client
    1. Open a terminal and run this command <br>
    ``` mosquitto_pub -h localhost -p 1883 -t "Comunicacion" -m "get /SAM/STemperatura/ST1"    ```
- listen to message published by server
    1. Open a terminal and run this command with an id that refers to an actuator in the database (not a camera) <br>```mosquitto_sub -h localhost -t "/SAM/AAlarma/AA1"``` 

    