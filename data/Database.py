import sqlite3
from datetime import datetime


class Database:
    dispositivo_table = "Dispositivo"
    actuador_table = "Actuadores"
    sensor_table = "Sensores"
    alarma_table = "Alarma"
    camara_table = "Camara"
    camara_foreign_key = "Actuadores_ID"
    actuadores_foreign_key = "Dispositivo_ID"
    alarma_foreign_key = "Actuadores_ID"
    sensores_foreign_key = "Dispositivo_ID"

    def __init__(self):
        self.connection = None
        self.__connect_or_create_database_singleton()

        self.cursor = None
        self.__cursor_singleton()
        self.__create_tables_if_not_exists()

    def commit_change(func):
        def wrapper(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self.commit_change()
        return wrapper

    def __connect_or_create_database_singleton(self):
        if not self.connection:
            self.connection = sqlite3.connect('tt_project.db')

    def __cursor_singleton(self):
        if not self.cursor:
            self.cursor = self.connection.cursor()

    def __create_tables_if_not_exists(self):
        self.cursor.executescript("""
            CREATE TABLE IF NOT EXISTS Dispositivo(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Direccion VARCHAR(12),
            Fecha DATE
            );

            CREATE TABLE IF NOT EXISTS Actuadores(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Estado INT,
            Dispositivo_ID INTEGER,
            FOREIGN KEY (Dispositivo_ID) REFERENCES Dispositivo(ID)
            );

            CREATE TABLE IF NOT EXISTS Sensores(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Valor REAL,
            Dispositivo_ID INTEGER,
            FOREIGN KEY (Dispositivo_ID) REFERENCES Dispositivo(ID)
            );

            CREATE TABLE IF NOT EXISTS Alarma(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Mensaje VARCHAR(50),
            Actuadores_ID INTEGER,
            FOREIGN KEY (Actuadores_ID) REFERENCES Actuadores(ID)
            );

            CREATE TABLE IF NOT EXISTS Camara(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Archivo VARCHAR(50),
            Actuadores_ID INTEGER,
            FOREIGN KEY (Actuadores_ID) REFERENCES Actuadores(ID)
            );
        """)

    @commit_change
    def insert_into(self, table, values):
        self.cursor.executemany(
            "INSERT INTO " + table + " VALUES (null, ?,?)", values)

    @commit_change
    def update_row(self, table, foreign_column, id, new_values):
        column_names = self.cursor.execute(
            "SELECT * FROM " + table + " LIMIT 1")
        col_name = [i[0] for i in column_names.description][1:]
        set_query = []
        for index in range(len(new_values)):
            if not new_values[index]:
                continue
            query = ""
            if isinstance(new_values[index], str):
                query = f"{col_name[index]} = '{new_values[index]}'"
            else:
                query = f"{col_name[index]} = {new_values[index]}"
            set_query.append(query)
        final_query = ','.join(set_query)
        parsed_query = f"UPDATE {table} SET {final_query} WHERE {foreign_column} = {id}"
        self.cursor.execute(parsed_query)

    @commit_change
    def delete_from(self, table, ids):
        self.cursor.executemany(
            "DELETE FROM " + table + " WHERE ID = ?", ids)

    def select_all_from(self, table):
        return list(self.cursor.execute("SELECT * FROM " + table))
        
    def select_all_from_column(self, table, column):
        return list(self.cursor.execute(f"SELECT {column} FROM {table}"))
        
    def get_from(self, column, table, column_condition, value_condition):
        get_query = f"SELECT {column} FROM {table} WHERE {column_condition} = '{value_condition}'"
        return list(self.cursor.execute(get_query))
        
    
    def get_id_from_dispositivo_with_topic(self, topic):
        return self.get_from("ID", Database.dispositivo_table, "Direccion", topic)[0][0]
        
    def get_id_from_actuador_with_device_id(self, device_id):
        return self.get_from("ID", Database.actuador_table, "Dispositivo_ID", device_id)[0][0]
        
    def get_valor_from_sensores_with_device_id(self, device_id):
        return self.get_from("Valor", Database.sensor_table, "Dispositivo_ID", device_id)[0][0]
        
    def get_archivo_from_camara_with_actuador_id(self, actuador_id):
        return self.get_from("Archivo", Database.camara_table, "Actuadores_ID", actuador_id)[0][0]
        
    def get_all_topics(self):
        return self.select_all_from_column(Database.dispositivo_table,"Direccion")
    
    def update_actuadores_with(self, device_id, new_state):
        self.update_row(Database.actuador_table, Database.actuadores_foreign_key, device_id,[int(new_state),None])
    
    def update_sensor_table_using(self, device_id, sensor_value):
        self.update_row(Database.sensor_table, Database.sensores_foreign_key,device_id, [float(sensor_value),None])
    
    def update_alarma_table_using(self,actuador_id, new_message):
        self.update_row(Database.alarma_table, Database.alarma_foreign_key ,actuador_id,[new_message,None])

        

    def commit_change(self):
        self.connection.commit()

    def close_connection(self):
        self.connection.close()