from block_io import BlockIo
import sqlite3
def get_new_wallet(user_id):
    block_io = BlockIo('beb5-768d-7b2c-1c0f', 'p26Mj6LEaiFZNSZs')
    wallet_dic = block_io.get_new_address(label=f'{user_id}')
    w = wallet_dic['data']
    wallet = w['address']
    connection = sqlite3.connect('db/database.db')
    cursor = connection.cursor()
    args = (wallet, user_id)
    try:
        cursor.execute('''Update users set wallet = ? where id_user = ?''',args)
        connection.commit()
        cursor.close()
    except:
        cursor.execute(f'''SELECT wallet from users where id_user ={user_id}''')
        exist_wallet = cursor.fetchone()
        cursor.close()

block_io = BlockIo('beb5-768d-7b2c-1c0f', 'p26Mj6LEaiFZNSZs')
#

#
# price = block_io.get_current_price(price_base='usd')['data']
# usd = price['prices'][0]['price']
# usd = float(usd)
# print(type(usd))
# connection = sqlite3.connect('db/database.db')
# cursor = connection.cursor()
# cursor.execute('''SELECT balance from users where id_user = 1143092873''')
# balance = cursor.fetchone()
# b = list(balance)[0]
# b = float(b)
# print(b)

connection = sqlite3.connect('db/database.db')
booking = connection.cursor()
booking.execute("SELECT booking from products where id_product = 10")
booking_check = booking.fetchone()
booking_check = list(booking_check)
booking_check = booking_check[0]
print(booking_check)