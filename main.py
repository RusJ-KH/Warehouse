import tkinter as tk
from tkinter import *
from tkinter import ttk


def some_callback_function():
    return


def some_other_callback_function():
    return


def getCargo():
    return

def getHumidState():
    humidityValueMinEntry.config(state=getHumidCheckBtnValue.get())
    humidityValueMaxEntry.config(state=getHumidCheckBtnValue.get())



# Create the root window
root = tk.Tk()
h = 720
w = 1600
root.geometry(f"{w}x{h}")
root.resizable(False, False)
root.title("Warehouse Information System")

# Create a menu bar
menubar = tk.Menu(root)
# Create a File menu
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

frame_top = Frame(root)
frame_middle = Frame(root)
frame_bot = Frame(root)

databaseNotebook = ttk.Notebook(frame_bot)
logTab = tk.Frame(databaseNotebook, width=300, height=200)
stockTab = tk.Frame(databaseNotebook, width=300, height=200)
databaseNotebook.add(logTab, text="История")
databaseNotebook.add(stockTab, text="Склад")
databaseNotebook.pack(side="top", fill="both", expand=True)

# label1 = Label(frame_top, text='frame_top')
# label1.pack()

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
storagePlacementLabel = Label(getTab, text='Расположение на складе')
storagePlacementLabel.grid(row=2, column=2)
storagePlacementEntry = Entry(getTab)
storagePlacementEntry.grid(row=2, column=3)
sendData = Button(getTab, text='Добавить в базу', command=getCargo)
sendData.grid(row=3, column=2, columnspan=2, sticky='we')

getHumidCheckBtnValue = StringVar()
getHumidCheckBtnValue.set('disabled')
humidityCheckbutton = Checkbutton(getTab, text='Учитывать влажность', variable=getHumidCheckBtnValue, command=getHumidState, onvalue='normal', offvalue='disabled')
humidityCheckbutton.grid(row=0, column=4)
humidityValueMinLabel = Label(getTab, text='От (%)', justify='right')
humidityValueMinLabel.grid(row=1,column=4)
humidityValueMinEntry = Entry(getTab, state=getHumidCheckBtnValue.get())
humidityValueMinEntry.grid(row=1, column=5)
humidityValueMaxLabel = Label(getTab, text='До (%)', justify='right')
humidityValueMaxLabel.grid(row=2,column=4)
humidityValueMaxEntry = Entry(getTab, state=getHumidCheckBtnValue.get())
humidityValueMaxEntry.grid(row=2, column=5)





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
