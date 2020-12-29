# testing commands
- add new device
    1. Add a new alarm: ```mosquitto_pub -h localhost -p 1883 -t "NuevosDispositivos" -m "/AA/H123" ```  you need to change the -m string to add differeent types of devices with this format <br>
    Types of devices: <br>
    /ST/T612   Sensor <br>
    /SP/Y481   Sensor  <br>
    /SL/3781   Sensor <br>
    /AP/4712   Actuator <br>
    /AE/ASDA   Actuator <br>
    /AA/RTYU   Alarma <br>
    /AC/JKTI   Camara <br>

- listen and insert value on database from topic
    1. Select a valid topic from the devices table
    2. Publish a value for that device in its topic ```mosquitto_pub -h localhost -p 1883 -t "/ST/T612" -m "10" ```

- delete a device
    1. Select a valid device from the devices table
    2. Publish that device's id to the "BorrarDispositivo" topic ```mosquitto_pub -h localhost -p 1883 -t "BorrarDispositivo" -m "/ST/T612 ```


    