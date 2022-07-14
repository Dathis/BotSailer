import sqlite3

connection = sqlite3.connect('db/database.db')
cursor = connection.cursor()
cursor.execute(f"SELECT balance from users where id_user ={1143092873}")
balance = cursor.fetchall()
balance = str(balance)
balance = balance.replace('[(','').replace(',)]','')