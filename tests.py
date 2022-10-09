from cityGame import checkDataToNotify
import requests
from datetime import date
import sqlite3
import unittest

class TestMyTest(unittest.TestCase):
  def test_AOpenMain(self):
    response = requests.get("http://127.0.0.1:5000")
    self.assertEqual(response.status_code, 200)

  def test_BAddFriend(self):
    current_date = str(date.today())
    response = requests.post("http://127.0.0.1:5000/addFriend", data={'frName':'БАЛАБАКИН АРТЕМ', 'frDate':current_date})
    self.assertEqual(response.status_code, 200)

  def test_CNotify(self):
    res = checkDataToNotify(debug=True)
    self.assertEqual(res, "ok")

  def test_DDelFriend(self):
    con = sqlite3.connect('mydatabase.db')
    cursorObj = con.cursor()
    sql = '''SELECT id FROM friendsBirthdayDates ORDER BY id DESC LIMIT 1'''
    cursorObj.execute(sql)
    data = cursorObj.fetchone()
    cursorObj.close()
    response = requests.post("http://127.0.0.1:5000/delFriend", data={'toDel':str(data[0])})
    self.assertEqual(response.status_code, 200)


unittest.main()