import sqlite3

connection = sqlite3.connect('chinook.db')

# create database
cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS Shows
              (Title TEXT, Director TEXT, Year INT)''')


#cursor.execute('''INSERT INTO Shows (Title, Director, Year) VALUES (%s,%s,%s)''', ("Testtitel", "ich", 2003))


connection.commit()

cursor.execute("SELECT * FROM sqlite_master WHERE type='table';")
for x in cursor:
    print(x)

connection.close()