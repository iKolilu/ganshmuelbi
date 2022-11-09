import uuid

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="billdb"
)

mycursor = mydb.cursor()

def connect():
  # TODO: implement this 
  return True


def get_provider(id):
  return "Not implemented"

def create_provider(name):
  sql = "INSERT INTO Provider (id, name) VALUES (%s, %s);"
  val = (None, name)
  mycursor.execute(sql, val)
  mydb.commit()

  return mycursor.lastrowid

def update_provider(id, name):
  sql = "UPDATE Provider SET name = %s WHERE id = %s;"
  val = (name, id)
  mycursor.execute(sql, val)
  mydb.commit()

  return mycursor.lastrowid
