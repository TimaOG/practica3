from flask import Flask, request, render_template, url_for
import sqlite3
from threading import Thread
import time
from datetime import date
from plyer import notification

app = Flask(__name__)


@app.route('/')
def start():
	dataToShow = getAllBD()
	return render_template('index.html', data=dataToShow)

@app.route('/addFriend', methods = ['POST', 'GET'])
def addFriend():
	if request.method == 'POST':
		friendName = request.form['frName']
		friendDate = request.form['frDate']
		addBD(friendName, friendDate)
	dataToShow = getAllBD()
	return render_template('index.html', data=dataToShow)

@app.route('/delFriend', methods = ['POST', 'GET'])
def delFriend():
	if request.method == 'POST':
		friendToDel = request.form['toDel']
		print(friendToDel)
		delBD(int(friendToDel))
	dataToShow = getAllBD()
	return render_template('index.html', data=dataToShow)



def addBD(frName, frDate):
	con = sqlite3.connect('mydatabase.db')
	cursorObj = con.cursor()
	sql = '''INSERT INTO friendsBirthdayDates (friendName, birthdayDate) VALUES (?, ?)'''
	dateTuple = (frName, frDate)
	cursorObj.execute(sql, dateTuple)
	con.commit()

def delBD(delId):
	con = sqlite3.connect('mydatabase.db')
	cursorObj = con.cursor()
	sql = '''DELETE FROM friendsBirthdayDates WHERE id = ?'''
	dateTuple = (delId,)
	cursorObj.execute(sql, dateTuple)
	con.commit()

def getBD(getId):
	con = sqlite3.connect('mydatabase.db')
	cursorObj = con.cursor()
	sql = '''SELECT friendName FROM friendsBirthdayDates WHERE id = ?'''
	dateTuple = (getId,)
	cursorObj.execute(sql, dateTuple)
	date = cursorObj.fetchone()
	cursorObj.close()
	return date

def getAllBD():
	con = sqlite3.connect('mydatabase.db')
	cursorObj = con.cursor()
	sql = '''SELECT * FROM friendsBirthdayDates'''
	cursorObj.execute(sql)
	date = cursorObj.fetchall()
	cursorObj.close()
	return date


def checkDataToNotify(debug=False):
	dataToCheck = getAllBD()
	current_date = str(date.today())[5:]
	for d in dataToCheck:
		if current_date == str(d[2][5:]):
			text = "Сегодня день рождение у " + d[1]
			notification.notify(title='Напоминание', message=text)
	if debug:
		return "ok"
	time.sleep(86400)
	checkDataToNotify()

def runServe():
	app.run()

if __name__ == "__main__":
	thread1 = Thread(target=checkDataToNotify)
	thread2 = Thread(target=runServe)
	thread1.start()
	thread2.start()
	thread1.join()
	thread2.join()