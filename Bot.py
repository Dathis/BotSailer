import time
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import ContentType
from add_states import Add_States, Delete_States, Update_States, Help, Hello, Alert
from config import token
import keyboards as kb
import sqlite3
from block_io import BlockIo
import re

storage = MemoryStorage()

bot = Bot(token=token)
dp = Dispatcher(bot, storage=storage)

admins = [1143092873,646932957,995797110,5325678388]


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    connection = sqlite3.connect('db/database.db')
    cursor = connection.cursor()
    params = (message.from_user.id,message.from_user.username,message.from_user.first_name,0,message.chat.id)
    cursor.execute(f'SELECT greeting from admin_usage')
    greeting = cursor.fetchone()
    greetings = str(greeting).replace("('", '').replace("',)", '')
    try:
        cursor.execute('''INSERT INTO users VALUES(?,?,?,?,Null,?)''', params)
        connection.commit()
        cursor.close()
    except:
        cursor.close()
    if message.from_user.id in admins:
        await message.reply(f"{greetings}",reply_markup=kb.admin_menu)
    else:
        await message.reply(f"{greetings}",reply_markup=kb.menu)

    print(message.from_user.first_name, message.from_user.id)


@dp.callback_query_handler(lambda query: query.data == 'menu', state='*')
async def done(query: types.CallbackQuery,state:FSMContext):
    connection = sqlite3.connect('db/database.db')
    cursor = connection.cursor()
    cursor.execute(f'SELECT greeting from admin_usage')
    greeting = cursor.fetchone()
    greetings = str(greeting).replace("('", '').replace("',)", '')
    if query.from_user.id in admins:
        await query.message.answer(f"{greetings}",reply_markup=kb.admin_menu)
    else:
        await query.message.answer(f"{greetings}",reply_markup=kb.menu)

@dp.message_handler(text="🧑‍💻Меню Администратора")
async def bot_message(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, 'Добро пожаловать в меню Администратора. Ваше меню изменилось.\nВыберите что вы хотите сделать', reply_markup=kb.admin_panel)

@dp.message_handler(text="🔸Отослать обьявление всем пользователям")
async def bot_message(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, 'Это сообщение отправится всем пользователям бота\nВведите сообщение:')
    await Alert.alert.set()

@dp.message_handler(state=Alert.alert)
async def bot_message(message: types.Message, state: FSMContext):
    alert = message.text
    connection = sqlite3.connect('db/database.db')
    cursor = connection.cursor()
    cursor.execute(f'SELECT chat_id from users')
    chat_id = cursor.fetchall()
    print(chat_id)
    for i in chat_id:
        i = list(i)
        await bot.send_message(i[0],f'{alert}')

@dp.message_handler(text="➕Добавить товар")
async def bot_message(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, 'Отлично,вы начали процедуру добавления товара.\nOтправьте мне имя продукта')
    await Add_States.name.set()


@dp.message_handler(state=Add_States.name)
async def get_name(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, 'Теперь отправьте мне описание')
    async with state.proxy() as data:
        data['name'] = message.text
    await Add_States.description.set()


@dp.message_handler(state=Add_States.description)
async def get_description(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, 'Теперь отправьте мне цену')
    async with state.proxy() as data:
        data['description'] = message.text
    await Add_States.price.set()


@dp.message_handler(state=Add_States.price)
async def get_price(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, 'Теперь отправьте мне Фотографию товара',reply_markup=kb.img_skip)
    async with state.proxy() as data:
        data['price'] = message.text
    await Add_States.img.set()


@dp.message_handler(state=Add_States.img, content_types=ContentType.PHOTO)
async def get_photo(message: types.Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    async with state.proxy() as data:
        data['img'] = file_id
    await bot.send_message(message.from_user.id, 'Теперь отправьте мне Город в котором находится товар.')
    await Add_States.adres.set()

@dp.callback_query_handler(lambda query: query.data == 'img_skip', state=Add_States.img)
async  def get_location(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, 'Теперь отправьте мне Город в котором находится товар."')
    await Add_States.adres.set()

@dp.message_handler(state=Add_States.adres)
async def get_location1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['city'] = message.text
    await bot.send_message(message.from_user.id,'Теперь отправьте мне адресс например:Улица Пушкина,4')
    await Add_States.url.set()

@dp.message_handler(state=Add_States.url)
async def get_url(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['adres'] = message.text
    await bot.send_message(message.from_user.id, 'Теперь отправьте мне ссылку на товар для покупателя')
    await Add_States.finish.set()

@dp.message_handler(state=Add_States.finish)
async def get_location1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['url'] = message.text
    await bot.send_message(message.from_user.id,'Товар готов к размещению нажмите на кнопку',reply_markup=kb.done)

@dp.callback_query_handler(lambda query: query.data == 'done', state='*')
async def done(query: types.CallbackQuery,state:FSMContext):
    await query.message.answer(f"Здравствуйте,{query.from_user.first_name}.\nВыберите интересующий вас раздел",
                                reply_markup=kb.admin_menu)
    async with state.proxy() as data:
        name = data.get('name')
        img = data.get('img')
        description = data.get('description')
        price = data.get('price')
        city = data.get('city')
        adres = data.get('adres')
        url = data.get('url')
        params = (name, img, description, price, city, adres, url,0)
        connection = sqlite3.connect('db/database.db')
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO products VALUES(Null,?,?,?,?,?,?,?,?)''', params)
        connection.commit()
        cursor.close()
    await state.finish()

@dp.message_handler(text="➖Удалить товар")
async def delete_product(message: types.Message):
    connection = sqlite3.connect('db/database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM products where booking = 0')
    exists = cursor.fetchall()
    for i in exists:
        await bot.send_message(message.chat.id, f'{i[0]}. {i[1]}-💸{i[4]} руб.\n{i[3]}\nГород:{i[5]}\nАдрес:{i[6]}')
    cursor.close()
    await bot.send_message(message.chat.id,'Введите id товара который хотите удалить')
    await Delete_States.delete.set()

@dp.message_handler(state=Delete_States.delete)
async def delete_product(message: types.Message, state: FSMContext):
    id = message.text
    connection = sqlite3.connect('db/database.db')
    cursor = connection.cursor()
    try:
        cursor.execute(f"""DELETE from products where id_product = {int(id)}""")
        connection.commit()
        await bot.send_message(message.chat.id,'Товар успешно удален')
        cursor.close()
    except:
        await bot.send_message(message.chat.id,'Произошла Ошибка. Проверьте корректность ввода данных')
    await state.finish()

@dp.message_handler(text="🆙Редактировать товар")
async def delete_product(message: types.Message):
    connection = sqlite3.connect('db/database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM products where booking = 0')
    exists = cursor.fetchall()
    for i in exists:
        await bot.send_message(message.chat.id, f'{i[0]}. {i[1]}-💸{i[4]} руб.\n{i[3]}\nГород:{i[5]}\nАдрес:{i[6]}')
    cursor.close()
    await bot.send_message(message.chat.id,'Введите id товара который хотите редактировать')
    await Update_States.update.set()

@dp.message_handler(state=Update_States.update)
async def update_product(message: types.Message, state: FSMContext):
    id = message.text
    async with state.proxy() as data:
        data['id'] = id
    connection = sqlite3.connect('db/database.db')
    cursor = connection.cursor()
    try:
        cursor.execute(f"""SELECT * from products where id_product = {int(id)}""")
        products = cursor.fetchone()
        p = list(products)
        await bot.send_message(message.chat.id,f'id:{p[0]}\nИмя:{p[1]}\nОписание:{p[3]}\nЦена:{p[4]} ₽\nГород:{p[5]}\nАдрес:{p[6]}')
        await bot.send_message(message.chat.id,'Отправьте раздел который вы хотите редактировать')
        await Update_States.choose.set()
    except:
        await bot.send_message(message.chat.id,'Что-то пошло не так')
        await state.finish()

@dp.message_handler(state=Update_States.choose)
async def update_product(message: types.Message, state: FSMContext):
    choose = message.text.title()
    if choose == 'Id':
        await bot.send_message(message.chat.id,'Извините,но id изменить нельзя в целях корректной работы базы данных\nВведите другой раздел')
        await Update_States.choose.set()
    elif choose == 'Имя':
        await bot.send_message(message.chat.id,'Введите новое имя')
        await Update_States.name.set()
    elif choose == 'Описание':
        await bot.send_message(message.chat.id,'Введите новое описание')
        await Update_States.description.set()
    elif choose == 'Цена':
        await bot.send_message(message.chat.id,'Введите новую цену')
        await Update_States.price.set()
    elif choose == 'Город':
        await bot.send_message(message.chat.id, 'Введите новый Город')
        await Update_States.city.set()
    elif choose == 'Адрес':
        await bot.send_message(message.chat.id, 'Введите новый адрес')
        await Update_States.adress.set()

    else:
        await bot.send_message(message.chat.id,'Вы ввели некорректные данные, попробуйте еще раз')


@dp.message_handler(state=Update_States.name)
async def update_product(message: types.Message, state: FSMContext):
    name = message.text
    connection = sqlite3.connect('db/database.db')
    cursor = connection.cursor()
    async with state.proxy() as data:
        args = (name, data['id'])
        cursor.execute('Update products set name = ? where id_product = ?',args)
    connection.commit()
    cursor.close()
    await bot.send_message(message.chat.id, 'Имя успешно заменено')
    await state.finish()

@dp.message_handler(state=Update_States.description)
async def update_product(message: types.Message, state: FSMContext):
    description = message.text
    connection = sqlite3.connect('db/database.db')
    cursor = connection.cursor()
    async with state.proxy() as data:
        args = (description, data['id'])
        cursor.execute('Update products set description = ? where id_product = ?', args)
    connection.commit()
    cursor.close()
    await bot.send_message(message.chat.id, 'Описание успешно заменено')
    await state.finish()


@dp.message_handler(state=Update_States.price)
async def update_product(message: types.Message, state: FSMContext):
    price = message.text
    connection = sqlite3.connect('db/database.db')
    cursor = connection.cursor()
    async with state.proxy() as data:
        args = (price, data['id'])
        cursor.execute('Update products set price = ? where id_product = ?', args)
    connection.commit()
    cursor.close()
    await bot.send_message(message.chat.id, 'Цена успешно заменена')
    await state.finish()

@dp.message_handler(state=Update_States.adress)
async def update_product(message: types.Message, state: FSMContext):
    adress = message.text
    connection = sqlite3.connect('db/database.db')
    cursor = connection.cursor()
    async with state.proxy() as data:
        args = (adress, data['id'])
        cursor.execute('Update products set adres = ? where id_product = ?', args)
    connection.commit()
    cursor.close()
    await bot.send_message(message.chat.id, 'Адрес успешно обновлен')
    await state.finish()

@dp.message_handler(state=Update_States.city)
async def update_product(message: types.Message, state: FSMContext):
    city = message.text
    connection = sqlite3.connect('db/database.db')
    cursor = connection.cursor()
    async with state.proxy() as data:
        args = (city, data['id'])
        cursor.execute('Update products set city = ? where id_product = ?', args)
    connection.commit()
    cursor.close()
    await bot.send_message(message.chat.id, 'Город успешно обновлен')
    await state.finish()


@dp.message_handler(text="🏠Меню")
async def bot_message(message: types.Message):
    connection = sqlite3.connect('db/database.db')
    cursor = connection.cursor()
    cursor.execute(f'SELECT greeting from admin_usage')
    greeting = cursor.fetchone()
    greetings = str(greeting).replace("('", '').replace("',)", '')
    if message.from_user.id in admins:
        await message.reply(f"{greetings}",reply_markup=kb.admin_menu)
    else:
        await message.reply(f"{greetings}",reply_markup=kb.menu)

@dp.message_handler(text="📦Все продукты")
async def bot_message(message: types.Message):
    connection = sqlite3.connect('db/database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products where booking = 0 ")
    products = cursor.fetchall()
    for product in products:
        p = list(product)
        try:
            await bot.send_photo(message.chat.id,photo=p[2],caption=f'{p[1]} 💸{p[4]} ₽\n{p[3]}\nГород:{p[5]}\nАдрес:{p[6]}\nid:{p[0]}',reply_markup=kb.product_kb)
        except:
            await bot.send_message(message.chat.id,f'{p[1]} 💸{p[4]} ₽\n{p[3]}\nГород:{p[5]}\nАдрес:{p[6]}\nid:{p[0]}',reply_markup=kb.product_kb)
    cursor.close()


@dp.callback_query_handler(lambda query: query.data == 'buy', state='*')
async def done(query: types.CallbackQuery,state:FSMContext):
    try:
        message = query.message.caption
        print(message)
        name = message.split('💸')
        print(name)
        name = name[0]
        id = re.findall(r'\d+', message)
        id = [int(i) for i in id]
        id = id[-1]
        async with state.proxy() as data:
            data['name'] = name
            data['id'] = id

        nums = re.findall(r'\d+', message)
        nums = [int(i) for i in nums]
        await query.message.answer(f'Подтвердите оплату товара\n С вашего баланса снимут: {nums[0]} ₽',reply_markup=kb.buy_proofs)

    except:
        message = query.message.text
        name = message.split('💸')
        print(name)
        name = name[0]
        id = re.findall(r'\d+', message)
        id = [int(i) for i in id]
        id = id[-1]
        async with state.proxy() as data:
            data['name'] = name
            data['id'] = id

        nums = re.findall(r'\d+', message)
        nums = [int(i) for i in nums]
        await query.message.answer(f'Подтвердите оплату товара\n С вашего баланса снимут: {nums[0]} ₽',reply_markup=kb.buy_proofs)


@dp.callback_query_handler(lambda query: query.data == 'aprove', state='*')
async def done(query: types.CallbackQuery,state:FSMContext):
    #Price on product
    message = query.message.text
    print(message)
    nums = re.findall(r'\d+', message)
    price = [int(i) for i in nums]
    price = price[0]
    user_id = query.from_user.id
    #BD
    connection = sqlite3.connect('db/database.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT balance FROM users where id_user ={user_id}")
    b = cursor.fetchone()
    balance = str(b).replace("(", '').replace(",)", '')
    balance = float(balance)
    connection = sqlite3.connect('db/database.db')
    booking = connection.cursor()
    booking.execute("SELECT booking from products where id_product = 10")
    booking_check = booking.fetchone()
    booking_check = list(booking_check)
    booking_check = booking_check[0]
    if price > balance:
        await bot.send_message(query.message.chat.id, f'⛔На вашем балансе недостаточно средств для покупки.\nСтоимость товара {price} ₽\nПополните свой баланс',reply_markup=kb.payment_kb)
    elif booking_check != 0:
        await bot.send_message(query.message.chat.id,'⛔К сожалению товар уже купили.')
    else:
        async with state.proxy() as data:
            id = data.get('id')
            cursor.execute(f"SELECT url FROM products where id_product ={id}",)
            url = cursor.fetchone()
            url = str(url).replace("('",'').replace("',)",'')
            balance = balance - price
            args = (balance, user_id)
            cursor.execute('''Update users set balance = ? where id_user = ?''', args)
            cursor.execute(f"Update products set booking = {user_id} where id_product={id}")
            connection.commit()
            cursor.close()
        await bot.send_message(query.message.chat.id,f'✅Вы успешно преобрели товар.\nС этой ссылкой вы можете поехать и забрать продукт\n{url}',disable_web_page_preview=True)

@dp.callback_query_handler(lambda query: query.data == 'cancel', state='*')
async def cancel(query: types.CallbackQuery,state:FSMContext):
    connection = sqlite3.connect('db/database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products where booking = 0")
    products = cursor.fetchall()
    for product in products:
        p = list(product)
        try:
            await bot.send_photo(query.message.chat.id,photo=p[2],caption=f'{p[1]} 💸{p[4]} ₽\n{p[3]}\nГород:{p[5]}\nАдрес:{p[6]}',reply_markup=kb.product_kb)
        except:
            await bot.send_message(query.message.chat.id,f'{p[1]} 💸{p[4]} ₽\n{p[3]}\nГород:{p[5]}\nАдрес:{p[6]}',reply_markup=kb.product_kb)
    cursor.close()


@dp.message_handler(text="🗺Города")
async def bot_message(message: types.Message):
    connection = sqlite3.connect('db/database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT city FROM products where booking =0")
    cities = cursor.fetchall()
    await bot.send_message(message.from_user.id, 'Снизу список городов в которых сейчас находятся некоторые товары.\nВыберите интересующий вас город', reply_markup=kb.genmarkup(cities))

@dp.callback_query_handler(lambda query: query.data.startswith("city"), state='*')
async def cities(query: types.CallbackQuery, state: FSMContext):
    city = query.data.split('_')
    connection = sqlite3.connect('db/database.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT * from products where city ='{city[1]}' and booking = 0")
    products = list(cursor.fetchall())
    for product in products:
        p = list(product)
        try:
            await bot.send_photo(query.message.chat.id,photo=p[2],caption=f'{p[1]} 💸{p[4]} ₽\n{p[3]}\nГород:{p[5]}\nАдрес:{p[6]}\nid:{p[0]}',reply_markup=kb.product_kb)
        except:
            await bot.send_message(query.message.chat.id,f'{p[1]} 💸{p[4]} ₽\n{p[3]}\nГород:{p[5]}\nАдрес:{p[6]}\nid:{p[0]}',reply_markup=kb.product_kb)
    cursor.close()





@dp.message_handler(text="💰Мой последний заказ")
async def bot_message(message: types.Message):
    connection = sqlite3.connect('db/database.db')
    cursor = connection.cursor()
    id = message.from_user.id
    cursor.execute(f"SELECT * from products where booking={id}")
    product = cursor.fetchall()
    for p in product:
        p = list(p)
        try:
            await bot.send_photo(message.chat.id, photo=p[2],
                                     caption=f'{p[1]} -💸{p[4]} ₽\n{p[3]}\nГород:{p[5]}\nАдрес:{p[6]}\nid:{p[0]}\n{p[7]}')
        except:
            await bot.send_message(message.chat.id,
                                       f'{p[1]} -💸{p[4]} ₽\n{p[3]}\nГород:{p[5]}\nАдрес:{p[6]}\nid:{p[0]}\n{p[7]}')


@dp.message_handler(text="❔Помощь")
async def bot_message(message: types.Message):
    connection = sqlite3.connect('db/database.db')
    cursor = connection.cursor()
    cursor.execute(f'SELECT help from admin_usage')
    help = cursor.fetchone()
    help_message = str(help).replace("('", '').replace("',)", '')
    await bot.send_message(message.from_user.id, f'{help_message}')


@dp.message_handler(text="💲Баланс")
async def bot_message(message: types.Message):
    id = message.from_user.id
    connection = sqlite3.connect('db/database.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT balance from users where id_user ={id}")
    balance = cursor.fetchall()
    balance = str(balance)
    balance = balance.replace('[(', '').replace(',)]', '')
    await bot.send_message(message.from_user.id, f'💰Ваш баланс:\n{balance} ₽')


@dp.message_handler(text="💶Пополнить Баланс")
async def bot_message(message: types.Message):
    await bot.send_message(message.chat.id, '💰Выберите оплату', reply_markup=kb.payment_kb)



@dp.callback_query_handler(lambda query: query.data == 'bitcoin', state='*')
async def bitcoin(query: types.CallbackQuery, state: FSMContext):
    user_id = query.from_user.id
    try:
        block_io = BlockIo('ac89-2470-8f58-f42c', 'p26Mj6LEaiFZNSZs')
        wallet_dic = block_io.get_new_address(label=f'{user_id}')
        w = wallet_dic['data']
        wallet = w['address']
        connection = sqlite3.connect('db/database.db')
        cursor = connection.cursor()
        args = (wallet, user_id)
        cursor.execute('''Update users set wallet = ? where id_user = ?''', args)
        connection.commit()
        await bot.send_message(query.message.chat.id,f'💰Отправьте желаемую для пополнения сумму на этот счет:\n{wallet}\nТекущий курс: 1 BTC - {rub} ₽\nМинимальное пополнение:0.00001 BTC',reply_markup=kb.pay_done)
        cursor.close()
    except:
        connection = sqlite3.connect('db/database.db')
        cursor = connection.cursor()
        cursor.execute(f'''SELECT wallet from users where id_user ={user_id}''')
        exist_wallet = cursor.fetchone()
        block_io = BlockIo('ac89-2470-8f58-f42c', 'p26Mj6LEaiFZNSZs')
        price = block_io.get_current_price(price_base='usd')['data']
        usd = price['prices'][0]['price']
        usd = float(usd)
        rub = usd * 65
        exist_wallet = str(exist_wallet).replace("('",'').replace("',)",'')
        await bot.send_message(query.message.chat.id,f'💰Отправьте желаемую для пополнения сумму на этот счет:\n{exist_wallet}\nТекущий курс: 1 BTC - {rub} ₽\nМинимальное пополнение:0.00001 BTC',reply_markup=kb.pay_done)
        cursor.close()


@dp.callback_query_handler(lambda query: query.data == 'payment_done', state='*')
async def payment_done(query: types.CallbackQuery, state: FSMContext):
    user_id = query.from_user.id
    block_io = BlockIo('ac89-2470-8f58-f42c', 'p26Mj6LEaiFZNSZs')
    wallet = block_io.get_address_balance(labels=f'{user_id}')
    b = wallet['data']
    wallet_bal = b['available_balance']
    wallet_bal = float(wallet_bal)
    price = block_io.get_current_price(price_base='usd')['data']
    usd = price['prices'][0]['price']
    usd = float(usd)
    rub = wallet_bal * usd
    rub = rub * 65
    connection = sqlite3.connect('db/database.db')
    cursor = connection.cursor()
    cursor.execute(f'SELECT balance from users where id_user={user_id}')
    balance = cursor.fetchone()
    b = list(balance)[0]
    b = float(b)
    rub = rub + b
    args = (rub, user_id)
    cursor.execute('''Update users set balance = ? where id_user = ?''', args)
    connection.commit()
    try:
        await bot.send_message(query.message.chat.id,f'⚜Вам зачислены деньги в размере {b} ₽⚜\n💰Ваш баланс сейчас \n{rub} ₽')
        transaction = block_io.prepare_transaction(amounts=f'{wallet_bal}', from_labels=f'{user_id}',
                                                   to_labels='default')
        time.sleep(0.2)
        create_transaction = block_io.create_and_sign_transaction(transaction)
        block_io.submit_transaction(transaction_data=create_transaction)
    except:
        await bot.send_message(query.message.chat.id,f'⛔Вы не пополнили счет, либо перевели сумму меньше чем 0.00001 BTC.\n💰Ваш баланс сейчас \n{rub} ₽')




@dp.message_handler(text="🔶Обновить приветственное сообщение")
async def bot_message(message: types.Message):
    await bot.send_message(message.chat.id, 'Отправьте новое Приветственное сообщение')
    await Hello.hello.set()

@dp.message_handler(state=Hello.hello)
async def update_product(message: types.Message, state: FSMContext):
    greetings = message.text
    connection = sqlite3.connect('db/database.db')
    cursor = connection.cursor()
    cursor.execute(f'Update admin_usage set greeting = "{greetings}"')
    connection.commit()
    cursor.close()
    await bot.send_message(message.chat.id, 'Приветственное сообщение было отредактировано')
    await state.finish()

@dp.message_handler(text="🔶Обновить раздел помощь")
async def bot_message(message: types.Message):
    await bot.send_message(message.chat.id, 'Отправьте новое сообщение для раздела Помощь')
    await Help.help.set()

@dp.message_handler(state=Help.help)
async def update_product(message: types.Message, state: FSMContext):
    help = message.text
    connection = sqlite3.connect('db/database.db')
    cursor = connection.cursor()
    cursor.execute(f'Update admin_usage set help = "{help}"')
    connection.commit()
    cursor.close()
    await bot.send_message(message.chat.id, 'Приветственное сообщение было отредактировано')
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
