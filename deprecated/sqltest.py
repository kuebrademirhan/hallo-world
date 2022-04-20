import mysql.connector
from datetime import datetime
import sqlite3

db = mysql.connector.connect(
    host="localhost",
    user="chris",
    passwd="chris",
    database="testdatabase"
)

mycursor = db.cursor()

# creation of a database
#mycursor.execute("CREATE DATABASE testdatabase")

# create table
# mycursor.execute("CREATE TABLE Person(name VARCHAR(50), age smallint UNSIGNED, personID int PRIMARY KEY AUTO_INCREMENT)")
#mycursor.execute("CREATE TABLE Test (name varchar(50) NOT NULL, created datetime NOT NULL, "
#                 "gender ENUM('M', 'F', 'O') NOT NULL, id int PRIMARY KEY NOT NULL AUTO_INCREMENT)")

# add content
#mycursor.execute("INSERT INTO Person (name, age) VALUES ('holger', 34)")
#mycursor.execute("INSERT INTO Person (name, age) VALUES (%s,%s)", ("Joe", 4))
#mycursor.execute("INSERT INTO Test (name, created, gender) VALUES (%s, %s, %s)", ("Ben", datetime.now(), "M"))
#mycursor.execute("INSERT INTO Test (name, created, gender) VALUES (%s, %s, %s)", ("Chrisa", datetime.now(), "F"))
#mycursor.execute("INSERT INTO Test (name, created, gender) VALUES (%s, %s, %s)", ("Hermine", datetime.now(), "F"))
#db.commit()

# alter content
#mycursor.execute("ALTER TABLE Test ADD COLUMN food VARCHAR(50) NOT NULL")

# delete column
#mycursor.execute("ALTER TABLE Test DROP COLUMN food")

# print tables
print("description of <Test> table:")
mycursor.execute("DESCRIBE Test")
for x in mycursor:
    print(x)

# print content
print("content:")
mycursor.execute("SELECT * FROM Test WHERE gender = 'M' ORDER BY id DESC")
for x in mycursor:
    print(x)

 

print ("ende!")