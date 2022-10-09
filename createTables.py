import sqlite3

con = sqlite3.connect('mydatabase.db')

cursorObj = con.cursor()

cursorObj.execute('''DROP TABLE IF EXISTS friendsBirthdayDates;''')

cursorObj.execute('''CREATE TABLE friendsBirthdayDates(
	id integer PRIMARY KEY AUTOINCREMENT, 
	friendName text, 
	birthdayDate date)''')
 
con.commit()