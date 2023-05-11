import tkinter as tk
import datetime
from tkinter import *
from tkinter import ttk

from dbinterface import *


def some_callback_function():
    return


def some_other_callback_function():
    return


def setCargo():
    code, errMsg = checkInputs()
    errorAlert(errMsg)
    if code == 0:
        insert_in_table(create_cargo_no_id(
            cargoNameEntry.get(),
            quantityEntry.get(),
            vendorEntry.get(),
            recipientEntry.get(),
            arrivalDateEntry.get(),
            issueDateEntry.get(),
            buildingPlacementEntry.get(),
            shelfPlacementEntry.get(),
            rowPlacementEntry.get(),
            int(humidityValueMinEntry.get()),
            int(humidityValueMaxEntry.get())))
        displayDataBase(take_from_table(con), stockTabDataFrame)
        stockTabCanvas.configure(scrollregion=stockTabCanvas.bbox("all"))
        clearEntry()


def checkInputs():
    if not (quantityEntry.get().isdigit() and int(quantityEntry.get()) > 0):
        return 1, 'Неверное значение количества товара'
    try:
        datetime.strptime(arrivalDateEntry.get(), "%Y-%m-%d")
    except ValueError:
        return 1, 'Неверно введена дата поставки. Используйте формат YY-MM-DD'
    try:
        datetime.strptime(issueDateEntry.get(), "%Y-%m-%d")
    except ValueError:
        return 1, 'Неверно введена дата отправления. Используйте формат YY-MM-DD'
    if datetime.strptime(arrivalDateEntry.get(), "%Y-%m-%d") > datetime.strptime(issueDateEntry.get(), "%Y-%m-%d"):
        # Здесь должен быть код ошибки
        return 1, 'Дата поставки не может быть позже даты отправления'
    if not buildingPlacementEntry.get().isalpha():
        return 1, 'Название помещения должно состоять из букв'
    if not (rowPlacementEntry.get().isdigit() and int(rowPlacementEntry.get()) > 0):
        return 1, 'Неверный номер ряда'
    if not (shelfPlacementEntry.get().isdigit() and int(shelfPlacementEntry.get()) > 0):
        return 1, 'Неверный номер полки'
    if not (humidityValueMinEntry.get().isdigit() and int(humidityValueMinEntry.get()) > 0):
        return 1, 'Неверное значение для минимальной допустимой влажности помещения'
    if not (humidityValueMaxEntry.get().isdigit() and int(humidityValueMaxEntry.get()) > 0):
        return 1, 'Неверное значение для максимальной допустимой влажности помещения'
    if int(humidityValueMaxEntry.get()) < int(humidityValueMinEntry.get()):
        return 1, 'Максимальная допустимая влажность помещения не должна быть меньше минимальной'
    return 0, ''


def clearEntry():
    cargoNameEntry.config(textvariable='')
    quantityEntry.config(textvariable='')
    vendorEntry.config(textvariable='')
    recipientEntry.config(textvariable='')
    arrivalDateEntry.config(textvariable='')
    issueDateEntry.config(textvariable='')
    buildingPlacementEntry.config(textvariable='')
    shelfPlacementEntry.config(textvariable='')
    rowPlacementEntry.config(textvariable='')
    humidityValueMinEntry.config(textvariable='')
    humidityValueMaxEntry.config(textvariable='')


def errorAlert(errMsg):
    l.config(text=errMsg)


def getHumidState():
    humidityValueMinEntry.config(state=getHumidCheckBtnValue.get())
    humidityValueMaxEntry.config(state=getHumidCheckBtnValue.get())


def display_data_line(frame, data_line, row):
    humidity_range = f'{data_line.min_humidity}-{data_line.max_humidity}%'
    storage_placement = f'{data_line.location_building}-{data_line.location_row}-{data_line.location_shelf}'
    # Create labels for each field and add them to the frame using grid layout
    tk.Label(frame, text=data_line.cargo_id).grid(row=row, column=0)
    ttk.Separator(frame, orient="vertical").grid(row=row, column=1, sticky="ns")
    tk.Label(frame, text=data_line.name, wraplength=150).grid(row=row, column=2)
    ttk.Separator(frame, orient="vertical").grid(row=row, column=3, sticky="ns")
    tk.Label(frame, text=data_line.amount).grid(row=row, column=4)
    ttk.Separator(frame, orient="vertical").grid(row=row, column=5, sticky="ns")
    tk.Label(frame, text=data_line.date_of_receiving).grid(row=row, column=6)
    ttk.Separator(frame, orient="vertical").grid(row=row, column=7, sticky="ns")
    tk.Label(frame, text=data_line.departure_date).grid(row=row, column=8)
    ttk.Separator(frame, orient="vertical").grid(row=row, column=9, sticky="ns")
    tk.Label(frame, text=humidity_range).grid(row=row, column=10)
    ttk.Separator(frame, orient="vertical").grid(row=row, column=11, sticky="ns")
    tk.Label(frame, text=storage_placement).grid(row=row, column=12)
    ttk.Separator(frame, orient="vertical").grid(row=row, column=13, sticky="ns")
    tk.Label(frame, text=data_line.provider, wraplength=150).grid(row=row, column=14)
    ttk.Separator(frame, orient="vertical").grid(row=row, column=15, sticky="ns")
    tk.Label(frame, text=data_line.recipient, wraplength=150).grid(row=row, column=16)
    ttk.Separator(frame, orient="horizontal").grid(row=row + 1, column=0, columnspan=17, sticky="we")


def display_data_top_bar(frame, tab: str):
    tk.Label(frame, text='ID', bg='#c4c4c4').grid(row=0, column=0)
    ttk.Separator(frame, orient="vertical").grid(row=0, column=1, sticky="ns")
    tk.Label(frame, text='Название товара', bg='#c4c4c4').grid(row=0, column=2)
    ttk.Separator(frame, orient="vertical").grid(row=0, column=3, sticky="ns")
    tk.Label(frame, text='Количество товара', bg='#c4c4c4').grid(row=0, column=4)
    ttk.Separator(frame, orient="vertical").grid(row=0, column=5, sticky="ns")
    tk.Label(frame, text='Дата поступления', bg='#c4c4c4').grid(row=0, column=6)
    ttk.Separator(frame, orient="vertical").grid(row=0, column=7, sticky="ns")
    tk.Label(frame, text='Дата отправления', bg='#c4c4c4').grid(row=0, column=8)
    ttk.Separator(frame, orient="vertical").grid(row=0, column=9, sticky="ns")
    tk.Label(frame, text='''Допустимая влажность 
    помещения''', bg='#c4c4c4').grid(row=0, column=10)
    ttk.Separator(frame, orient="vertical").grid(row=0, column=11, sticky="ns")
    tk.Label(frame, text='''Расположение товара
    на складе''', bg='#c4c4c4').grid(row=0, column=12)
    ttk.Separator(frame, orient="vertical").grid(row=0, column=13, sticky="ns")
    tk.Label(frame, text='Поставщик', bg='#c4c4c4').grid(row=0, column=14)
    ttk.Separator(frame, orient="vertical").grid(row=0, column=15, sticky="ns")
    tk.Label(frame, text='Получатель', bg='#c4c4c4').grid(row=0, column=16)
    ttk.Separator(frame, orient="horizontal").grid(row=1, column=0, columnspan=17, sticky="we")


def configureDataColumns(frame, tab: str):
    frame.columnconfigure(0, minsize=50)
    frame.columnconfigure(2, minsize=150)
    frame.columnconfigure(4, minsize=130)
    frame.columnconfigure(6, minsize=130)
    frame.columnconfigure(8, minsize=130)
    frame.columnconfigure(10, minsize=160)
    frame.columnconfigure(12, minsize=160)
    frame.columnconfigure(14, minsize=160)
    frame.columnconfigure(16, minsize=160)


def displayDataBase(arr, frame):
    for i in range(len(arr)):
        display_data_line(frame, arr[i], i * 2)

listeners = []
def dateListen(arr):
    for i in range(len(arr)):
        listeners.append(dateListener(arr[i]))
        arr[i].coming_date()


def clearFrame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def updateLog():
    clearFrame(logTabDataFrame)
    displayDataBase(take_from_table(con2), logTabDataFrame)
    logTabCanvas.configure(scrollregion=logTabCanvas.bbox("all"))


def getDate():
    dateListen(take_from_table(con))
    clearFrame(stockTabDataFrame)
    displayDataBase(take_from_table(con), stockTabDataFrame)

    clearFrame(logTabDataFrame)
    displayDataBase(take_from_table(con2), logTabDataFrame)
    logTabCanvas.configure(scrollregion=logTabCanvas.bbox("all"))

    root.after(5000, getDate)


# Create the root window
root = tk.Tk()


h = 720
w = 1270
root.geometry(f"{w}x{h}")
root.resizable(False, False)
root.title("Warehouse Information System")

# -Create a menu bar----------------------------------------------------------
menubar = tk.Menu(root)

# -Create a File menu----------------------------------------------------------
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=some_callback_function)
filemenu.add_command(label="Save", command=some_other_callback_function)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
# Add the File menu to the menu bar
menubar.add_cascade(label="File", menu=filemenu)
# Create an Edit menu
editmenu = tk.Menu(menubar, tearoff=0)
editmenu.add_command(label="Undo", command=some_callback_function)
editmenu.add_command(label="Redo", command=some_other_callback_function)
# Add the Edit menu to the menu bar
menubar.add_cascade(label="Edit", menu=editmenu)
# Attach the menu bar to the root window
root.config(menu=menubar)

# -Create main Frames----------------------------------------------------------
frame_top = Frame(root)
frame_middle = Frame(root)
frame_bot = Frame(root)

# -Create Tabs-----------------------------------------------------------------
databaseNotebook = ttk.Notebook(frame_bot)
logTab = tk.Frame(databaseNotebook, width=300, height=200)
stockTab = tk.Frame(databaseNotebook, width=300, height=200)
databaseNotebook.add(stockTab, text="Склад")
databaseNotebook.add(logTab, text="История")
databaseNotebook.pack(side="top", fill="both", expand=True)
# -----------------------------------------------------------------------------
dataInterfaceNotebook = ttk.Notebook(frame_middle)
getTab = tk.Frame(dataInterfaceNotebook, width=300, height=200)
sendTab = tk.Frame(dataInterfaceNotebook, width=300, height=200)
dataInterfaceNotebook.add(getTab, text="Принять товар")
dataInterfaceNotebook.add(sendTab, text="Отправить товар")
dataInterfaceNotebook.pack(side="top", fill="both", expand=True)

# --------Middle Frame-----------------------------------------------------------------------------------
cargoNameLabel = Label(getTab, text='Название товара')
cargoNameLabel.grid(row=0, column=0)
cargoNameEntry = Entry(getTab)
cargoNameEntry.grid(row=0, column=1)
quantityLabel = Label(getTab, text='Количество товара')
quantityLabel.grid(row=1, column=0)
quantityEntry = Entry(getTab)
quantityEntry.grid(row=1, column=1)
vendorLabel = Label(getTab, text='Поставщик')
vendorLabel.grid(row=2, column=0)
vendorEntry = Entry(getTab)
vendorEntry.grid(row=2, column=1)
recipientLabel = Label(getTab, text='Получатель')
recipientLabel.grid(row=3, column=0)
recipientEntry = Entry(getTab)
recipientEntry.grid(row=3, column=1)
arrivalDateLabel = Label(getTab, text='Дата поставки')
arrivalDateLabel.grid(row=0, column=2)
arrivalDateEntry = Entry(getTab)
arrivalDateEntry.grid(row=0, column=3)
issueDateLabel = Label(getTab, text='Дата отправления')
issueDateLabel.grid(row=1, column=2)
issueDateEntry = Entry(getTab)
issueDateEntry.grid(row=1, column=3)
buildingPlacementLabel = Label(getTab, text='Помещение')
buildingPlacementLabel.grid(row=2, column=2)
buildingPlacementEntry = Entry(getTab)
buildingPlacementEntry.grid(row=2, column=3)
rowPlacementLabel = Label(getTab, text='Ряд')
rowPlacementLabel.grid(row=3, column=2)
rowPlacementEntry = Entry(getTab)
rowPlacementEntry.grid(row=3, column=3)
shelfPlacementLabel = Label(getTab, text='Полка')
shelfPlacementLabel.grid(row=4, column=2)
shelfPlacementEntry = Entry(getTab)
shelfPlacementEntry.grid(row=4, column=3)

sendData = Button(getTab, text='Добавить в базу', command=setCargo)
sendData.grid(row=4, column=0, columnspan=2, sticky='we')

humidityValueMinLabel = Label(getTab, text='От (%)', justify='right')
humidityValueMinLabel.grid(row=1, column=4)
humidityValueMinEntry = Entry(getTab)
humidityValueMinEntry.grid(row=1, column=5)
humidityValueMaxLabel = Label(getTab, text='До (%)', justify='right')
humidityValueMaxLabel.grid(row=2, column=4)
humidityValueMaxEntry = Entry(getTab)
humidityValueMaxEntry.grid(row=2, column=5)

# ErrMsg
l = Label(getTab, text='', fg='red')
l.grid(row=5, column=0, columnspan=10, sticky='we')

# -------------------------------------------------------------------------------------------------------
# sendTabButton = Button(sendTab, text='Обновить', command=updateLog)
# sendTabButton.pack(side='top')
# -------------------------------------------------------------------------------------------------------

stockTabFrame = Frame(stockTab)
stockTabTopFrame = Frame(stockTab, bg='#c4c4c4')  #
stockTabTopFrame.pack(anchor=NW)
stockTabCanvas = Canvas(stockTab)
stockTabCanvas.pack(side=LEFT, fill=BOTH, expand=1)
stockTabScrollbar = ttk.Scrollbar(stockTab, orient=VERTICAL, command=stockTabCanvas.yview)
stockTabScrollbar.pack(side=RIGHT, fill=Y)
stockTabCanvas.configure(yscrollcommand=stockTabScrollbar.set)
stockTabCanvas.bind('<Configure>', lambda e: stockTabCanvas.configure(scrollregion=stockTabCanvas.bbox("all")))
stockTabDataFrame = Frame(stockTabCanvas)  #
stockTabCanvas.create_window((0, 0), window=stockTabDataFrame, anchor=NW)
configureDataColumns(stockTabTopFrame, 'stockTab')
configureDataColumns(stockTabDataFrame, 'stockTab')
display_data_top_bar(stockTabTopFrame, 'stockTab')
displayDataBase(take_from_table(con), stockTabDataFrame)
stockTabFrame.pack(anchor=NW)

# -----------------------------

logTabFrame = Frame(logTab)
logTabTopFrame = Frame(logTab, bg='#c4c4c4')  #
logTabTopFrame.pack(anchor=NW)
logTabCanvas = Canvas(logTab)
logTabCanvas.pack(side=LEFT, fill=BOTH, expand=1)
logTabScrollbar = ttk.Scrollbar(logTab, orient=VERTICAL, command=logTabCanvas.yview)
logTabScrollbar.pack(side=RIGHT, fill=Y)
logTabCanvas.configure(yscrollcommand=logTabScrollbar.set)
logTabCanvas.bind('<Configure>', lambda e: logTabCanvas.configure(scrollregion=logTabCanvas.bbox("all")))
logTabDataFrame = Frame(logTabCanvas)
logTabCanvas.create_window((0, 0), window=logTabDataFrame, anchor=NW)
getDate()
configureDataColumns(logTabTopFrame, 'logTab')
configureDataColumns(logTabDataFrame, 'logTab')
display_data_top_bar(logTabTopFrame, 'logTab')
displayDataBase(take_from_table(con), stockTabDataFrame)
displayDataBase(take_from_table(con2), logTabDataFrame)
logTabFrame.pack(anchor=NW)

# -----------------------------

logTabTopFrame = Frame(logTabFrame, bg='#c4c4c4')
configureDataColumns(logTabDataFrame, 'logTab')
logTabTopFrame.pack(anchor=NW)
logTabFrame.pack(anchor=NW)

# -------------------------------------------------------------------------------------------------------
frame_top.grid(row=0, column=0, stick='wen')
frame_middle.grid(row=1, column=0, stick='we')
frame_bot.grid(row=2, column=0, stick='wens')
root.grid_columnconfigure(0, minsize=1600)
root.grid_rowconfigure(0, minsize=70)
root.grid_rowconfigure(1, minsize=300)
root.grid_rowconfigure(2, minsize=350)
# -------------------------------------------------------------------------------------------------------

root.mainloop()
