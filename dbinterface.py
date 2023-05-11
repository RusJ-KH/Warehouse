import sqlite3 as sl
from datetime import datetime

con = sl.connect('cargo.db')


def create_table():
    with con:
        con.execute("""
            CREATE TABLE CARGOS (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                amount INTEGER,
                provider TEXT,
                recipient TEXT,
                date_of_receiving DATE,
                departure_date DATE,
                location_building TEXT,
                location_shelf INTEGER,
                location_row INTEGER, 
                min_humidity INTEGER CHECK (min_humidity>=0 and min_humidity<=100),
                max_humidity INTEGER CHECK (max_humidity>=0 and max_humidity<=100)     
            );
        """)


def insert_in_table(id_cargo: int,
                    name: str,
                    amount: int,
                    provider: str,
                    recipient: str,
                    date_of_receiving: str,
                    departure_date: str,
                    location_building: str,
                    location_shelf: int,
                    location_row: int,
                    min_humidity: int,
                    max_humidity: int):
    try:
        datetime.strptime(date_of_receiving, "%Y-%m-%d")
        datetime.strptime(departure_date, "%Y-%m-%d")
    except ValueError:
        # Здесь должен быть код ошибки
        return
    if datetime.strptime(date_of_receiving, "%Y-%m-%d") > datetime.strptime(departure_date, "%Y-%m-%d"):
        # Здесь должен быть код ошибки
        return
    sql = 'INSERT INTO CARGOS (id, name, amount, provider, recipient, date_of_receiving, departure_date, ' \
        'location_building, location_shelf, location_row, min_humidity, max_humidity) values(?, ?, ?, ?, ?, ?, ?, ?, ' \
          '?, ?, ?, ?)'
    data = [(id_cargo,
             name,
             amount,
             provider,
             recipient,
             date_of_receiving,
             departure_date,
             location_building,
             location_shelf,
             location_row,
             min_humidity,
             max_humidity)]
    with con:
        con.executemany(sql, data)


def show_from_table():
    with con:
        data = con.execute("SELECT * FROM CARGOS")
        for row in data:
            print(row)


create_table()
insert_in_table(1, "Хуйня из-под коня", 33, "Мразота", "Уёба", "2022-12-05", "2022-03-05", "Нигде", 99, 11, 9, 10)
show_from_table()
