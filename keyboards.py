from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3
import time

menu = ReplyKeyboardMarkup(resize_keyboard=True,row_width=3)
menu.add(KeyboardButton('🏠Меню'))
menu.row(KeyboardButton('📦Все продукты'))
menu.insert(KeyboardButton('🗺Локации'))
menu.insert(KeyboardButton('💰Мой последний заказ'))
menu.insert(KeyboardButton('❔Помощь'))
menu.insert(KeyboardButton('💲Баланс'))
menu.insert(KeyboardButton('💶Пополнить Баланс'))

admin_menu =ReplyKeyboardMarkup(resize_keyboard=True,row_width=3)
admin_menu.add(KeyboardButton('🏠Меню'))
admin_menu.row(KeyboardButton('📦Все продукты'))
admin_menu.insert(KeyboardButton('🗺Города'))
admin_menu.insert(KeyboardButton('💰Мой последний заказ'))
admin_menu.insert(KeyboardButton('❔Помощь'))
admin_menu.insert(KeyboardButton('💲Баланс'))
admin_menu.insert(KeyboardButton('💶Пополнить Баланс'))
admin_menu.add(KeyboardButton('🧑‍💻Меню Администратора'))

admin_panel = ReplyKeyboardMarkup(resize_keyboard=True,row_width=3)
admin_panel.add('➕Добавить товар')
admin_panel.add('🆙Редактировать товар')
admin_panel.add('➖Удалить товар')
admin_panel.add('🔶Обновить приветственное сообщение')
admin_panel.add('🔶Обновить раздел помощь')
admin_panel.add('🔸Отослать обьявление всем пользователям')
admin_panel.add('🏠Меню')

admin_back = InlineKeyboardMarkup()
admin_back.add(InlineKeyboardButton('🏠Меню',callback_data='menu'))

done = InlineKeyboardMarkup()
done.add(InlineKeyboardButton('Разместить товар',callback_data='done'))

img_skip = InlineKeyboardMarkup()
img_skip.add(InlineKeyboardButton('Пропустить эту часть',callback_data='img_skip'))

product_kb = InlineKeyboardMarkup()
product_kb.add(InlineKeyboardButton('Купить',callback_data='buy'))

cities_kb = InlineKeyboardMarkup(row_width=3)



def genmarkup(cities):
    cities_kb = InlineKeyboardMarkup(row_width=1)
    cities = set(cities)
    cities = tuple(cities)
    for i in cities:
        i = str(i)
        i = i.replace("('", '').replace("',)", '')
        cities_kb.add(InlineKeyboardButton(i, callback_data=f'city_{i}'))
    return cities_kb

payment_kb = InlineKeyboardMarkup()
payment_kb.add(InlineKeyboardButton('Bitcoin',callback_data='bitcoin'))

pay_done = InlineKeyboardMarkup()
pay_done.add(InlineKeyboardButton('Оплачено',callback_data='payment_done'))


buy_proofs = InlineKeyboardMarkup()
buy_proofs.add(InlineKeyboardButton('Подтвердить',callback_data='aprove'))
buy_proofs.add(InlineKeyboardButton('Отменить',callback_data='cancel'))