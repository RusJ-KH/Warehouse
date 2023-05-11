import abc
from typing import List
import datetime

# Абстрактный класс наблюдателя, от него наследуется тот класс, который будет следить за датой
class IObserver(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def update(self, p: int):
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
    def notyfy(self):
        pass

# Пример наследования от класса IObservable
class Date(IObservable):
    def __init__(self, date):
        self.__date = date
        self.__observers = List[IObserver] = []
        self.notify()

    # Самое важное для класса Cargo.
    def change_date(self, date):
        self.__date = date
        self.notify()

    def add_observer(self, o: IObserver):
        self.__observers.append(o)

    def remove_observer(self, o: IObserver):
        self.__observers.remove(o)

    def notify(self):
        for o in self.__observers:
            o.update(self.__date)

class Someclass(IObserver):
    def __init__(self, obj: IObservable):
        self.__date = obj
        obj.add_observer(self)

    def update(self, p: int):
        if datetime.strptime(self.__date, "%Y-%m-%d") >= datetime.date.today():
            print("somthing is outdated")


