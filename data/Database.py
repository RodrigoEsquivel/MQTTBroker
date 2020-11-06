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
        
    def get_from(self, column, table, column_condition, value_condition):
        get_query = f"SELECT {column} FROM {table} WHERE {column_condition} = '{value_condition}'"
        return list(self.cursor.execute(get_query))

    def commit_change(self):
        self.connection.commit()

    def close_connection(self):
        self.connection.close()