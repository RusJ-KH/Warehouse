import sqlite3 as sl
import abc
import copy
import datetime
from typing import List
from datetime import datetime


# Абстрактный класс наблюдателя, от него наследуется тот класс, который будет следить за датой
class IObserver(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def update(self, date: str, id, ):
        pass


# Абстрактный класс наблюдаемого, от него будет наследоваться класс Cargo.
# также необходимо будет переопределить методы этого класса в классе Cargo (пример на классе Date ниже)
class IObservable(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def add_observer(self, o: IObserver):
        pass

    @abc.abstractmethod
    def remove_observer(self, o: IObserver):
        pass

    @abc.abstractmethod
    def notify(self):
        pass

class dateListener(IObserver):
    def __init__(self, obj: IObservable):
        self.__date = obj
        obj.add_observer(self)

    def update(self, date_: str, id):
        if str(date_) <= datetime.today().strftime("%Y-%m-%d"):
            print('some shit is happened', id)
            take_from_table(con)
            send_to_logs(id)
            self.__date.remove_observer(self)

#def

# Класс грузов:
class Cargo(IObservable):
    def __init__(self,
                 cargo_id: int,
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
        self.cargo_id = cargo_id
        self.name = name
        self.amount = amount
        self.provider = provider
        self.recipient = recipient
        self.date_of_receiving = date_of_receiving
        self.departure_date = departure_date
        self.location_building = location_building
        self.location_shelf = location_shelf
        self.location_row = location_row
        self.min_humidity = min_humidity
        self.max_humidity = max_humidity
        self.observers: List[IObserver] = []

    def clone(self):
        return copy.copy(self)

    def coming_date(self):
        self.notify()

    def add_observer(self, o: IObserver):
        self.observers.append(o)

    def remove_observer(self, o: IObserver):
        self.observers.remove(o)

    def notify(self):
        for o in self.observers:
            o.update(self.departure_date, self.cargo_id)

    def __del__(self):
        return 0


# Прототип груза:
prototype_cargo = Cargo(0, "", 0, "", "", "", "", "", 0, 0, 0, 0)



# Функция создания груза через копирование прототипа:
def create_cargo_no_id(name: str,
                       amount: int,
                       provider: str,
                       recipient: str,
                       date_of_receiving: str,
                       departure_date: str,
                       location_building: str,
                       location_shelf: int,
                       location_row: int,
                       min_humidity: int,
                       max_humidity: int) -> Cargo:
    # Создание нового груза через копирование прототипа:
    cargo = Cargo.clone(prototype_cargo)

    # Назначение переменных-элементов груза:
    cargo.name = name
    cargo.amount = amount
    cargo.provider = provider
    cargo.recipient = recipient
    cargo.date_of_receiving = date_of_receiving
    cargo.departure_date = departure_date
    cargo.location_building = location_building
    cargo.location_shelf = location_shelf
    cargo.location_row = location_row
    cargo.min_humidity = min_humidity
    cargo.max_humidity = max_humidity

    return cargo


con = sl.connect('cargo.db')
con2 = sl.connect('logcargo.db')


def create_table(con_in):
    with con_in:
        con_in.execute("""
            CREATE TABLE IF NOT EXISTS CARGOS (
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


def insert_in_table(cargo: Cargo):
    cargo_id = 0
    data = con.execute("SELECT EXISTS (SELECT 1 FROM CARGOS)")
    for row in data:
        if row[0] != 0:
            data2 = con.execute("SELECT * FROM CARGOS ORDER BY id DESC LIMIT 1")
            for row2 in data2:
                cargo_id = row2[0] + 1
        else:
            cargo_id = 1

    sql = 'INSERT INTO CARGOS (id, name, amount, provider, recipient, date_of_receiving, departure_date, ' \
          'location_building, location_shelf, location_row, min_humidity, max_humidity) values(?, ?, ?, ?, ?, ?, ?, ?, ' \
          '?, ?, ?, ?)'
    if cargo_id != 0:
        data = [(cargo_id,
                cargo.name,
                cargo.amount,
                cargo.provider,
                cargo.recipient,
                cargo.date_of_receiving,
                cargo.departure_date,
                cargo.location_building,
                cargo.location_shelf,
                cargo.location_row,
                cargo.min_humidity,
                cargo.max_humidity)]
        with con:
            con.executemany(sql, data)
    del cargo


def take_from_table(choose_con):
    cargos_list = []
    with choose_con:
        data = choose_con.execute("SELECT * FROM CARGOS")
        lst = data.fetchall()
    for j in range(0, len(lst)):
        cargo_entity = Cargo.clone(prototype_cargo)
        cargo_entity.cargo_id = lst[j][0]
        cargo_entity.name = lst[j][1]
        cargo_entity.amount = lst[j][2]
        cargo_entity.provider = lst[j][3]
        cargo_entity.recipient = lst[j][4]
        cargo_entity.date_of_receiving = lst[j][5]
        cargo_entity.departure_date = lst[j][6]
        cargo_entity.location_building = lst[j][7]
        cargo_entity.location_shelf = lst[j][8]
        cargo_entity.location_row = lst[j][9]
        cargo_entity.min_humidity = lst[j][10]
        cargo_entity.max_humidity = lst[j][11]
        cargos_list.append(cargo_entity)

    return cargos_list


def send_to_logs(sent_id: int):
    global glob_id
 #f"SELECT EXISTS (SELECT * FROM CARGOS WHERE id = {sent_id})"
    with con:
        data = con.execute(f"SELECT * FROM CARGOS WHERE id = {sent_id}")
        print(con.execute(f"SELECT * FROM CARGOS WHERE id = {sent_id}"))
        cargo_to_send = data.fetchone()

    data = con.execute(f"SELECT EXISTS (SELECT * FROM CARGOS WHERE id = {sent_id})")
    con.execute(f"DELETE FROM CARGOS WHERE id = {sent_id}")

    for row in data:
        print(row)
        if row[0] != 0:
            sql = 'INSERT OR IGNORE INTO CARGOS (id, name, amount, provider, recipient, date_of_receiving, departure_date, ' \
                  'location_building, location_shelf, location_row, min_humidity, max_humidity) values(?, ?, ?, ?, ?, ?, ?, ?, ' \
                  '?, ?, ?, ?)'
            data = [(glob_id,
                     cargo_to_send[1],
                     cargo_to_send[2],
                     cargo_to_send[3],
                     cargo_to_send[4],
                     cargo_to_send[5],
                     cargo_to_send[6],
                     cargo_to_send[7],
                     cargo_to_send[8],
                     cargo_to_send[9],
                     cargo_to_send[10],
                     cargo_to_send[11])]
            with con2:
                con2.executemany(sql, data)
            glob_id += 1


Crg = create_cargo_no_id('Шины Michelin X-Ice North 4 SUV 225/65 R17', 4, 'Michelin SCA', 'ИП Подъёмник', '2022-10-15', '2022-12-20', 'storage1',
                         2, 1, 10, 60)
Crg1 = create_cargo_no_id('Крыло правое переднее Nissan 350z', 1, 'ОАО Бокс-кит', 'ЗАО Автострой', '2022-9-15', '2023-1-13', 'storage1',
                         2, 2, 20, 50)
Crg2 = create_cargo_no_id('Привод передний ВАЗ-2107', 4, 'АО АвтоВАЗ', 'ИП Подъёмник', '2022-7-15', '2022-10-11', 'storage2',
                         3, 4, 10, 100)



glob_id = 1
create_table(con)
create_table(con2)
# insert_in_table(Crg)
# insert_in_table(Crg1)
# insert_in_table(Crg2)
