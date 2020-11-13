# testing commands
- add new device
    1. Add a new alarm: ```mosquitto_pub -h localhost -p 1883 -t "NuevosDispositivos" -m "/SAM/AAlarma/AA1" ```  you need to change the -m string to add differeent types of devices with this format <br>
    Types of devices: 
    /SAM/STemperatura/ST1  2 Sensor
    /SAM/SPresencia/SP1    2
    /SAM/SLiquido/SL1      2
    /SAM/APuerta/AP1       1 Other 
    /SAM/AEncendido/AE1    1
    /SAM/AAlarma/AA1       4 Alarma
    /SAM/ACamara/AC1       3 Camara
- sending value as a sensor
    1. Open a terminal and run this command: <br>``` mosquitto_pub -h localhost -p 1883 -t "/SAM/STemperatura/ST1" -m "20.01" ```
- sending ip as a camera
    1. Open a terminal and run this command: <br>
    ``` mosquitto_pub -h localhost -p 1883 -t "/SAM/ACamara/AC1" -m "192.168.1.1" ``` 
- set value as client
    1. Open a terminal and run this command <br>
    ```mosquitto_pub -h localhost -p 1883 -t "Comunicacion" -m "set /SAM/APuerta/AP1 9"```

- get value as client
    1. Open a terminal and run this command <br>
    ``` mosquitto_pub -h localhost -p 1883 -t "Comunicacion" -m "get /SAM/STemperatura/ST1"    ```
- listen to message published by server
    1. Open a terminal and run this command with an id that refers to an actuator in the database (not a camera) <br>```mosquitto_sub -h localhost -t "/SAM/AAlarma/AA1"``` 

    