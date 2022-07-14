from aiogram.dispatcher.filters.state import StatesGroup, State

class Add_States(StatesGroup):
    name = State()
    description = State()
    price = State()
    img = State()
    location1 = State()
    adres = State()
    url = State()
    finish = State()

class Delete_States(StatesGroup):
    delete = State()

class Update_States(StatesGroup):
    update = State()
    choose = State()
    name = State()
    description = State()
    price = State()
    adress = State()
    city = State()

class Balance(StatesGroup):
    balance = State()

class Hello(StatesGroup):
    hello = State()

class Help(StatesGroup):
    help = State()

class Alert(StatesGroup):
    alert = State()