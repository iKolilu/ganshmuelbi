import mysql.connector
from library import get_provider_id_long, get_provider_id_short


def connect():
  connection = None
  try:
    connection = mysql.connector.connect(
      host="mysql",
      port=3306,
      user="root",
      password="password",
      database="billdb"
    )
    print("MySQL Database connection successful")
  except mysql.Error as err:
    print(f"Error: '{err}'")

  return connection

def get_provider(connection, id):
  cursor = connection.cursor()
  sql = "SELECT * FROM Provider WHERE id = %s;"
  val = (id,)
  cursor.execute(sql, val)
  myresult = cursor.fetchone()

  return myresult


def get_one_rate(connection, product_id, scope):
  cursor = connection.cursor()
  sql = "SELECT * FROM Rates WHERE product_id = %s AND scope = %s;"
  val = (product_id, scope)

  cursor.execute(sql, val)
  myresult = cursor.fetchall()

  print(myresult)
  return myresult  

def get_all_rates(connection, product_id):
  cursor = connection.cursor()
  sql = "SELECT * FROM Rates;"

  cursor.execute(sql)
  myresult = cursor.fetchall()

  return myresult


def create_rates(connection, product_id, rate, scope):
  cursor = connection.cursor()
  sql = "INSERT INTO Rates (product_id, rate, scope) VALUES (%s, %s, %s);"
  val = (product_id, rate, scope)
  cursor.execute(sql, val)
  connection.commit()

  print(cursor.lastrowid)

  return cursor.lastrowid



def update_rates_same_pid_scope(connection, product_id, rate, scope):
  cursor = connection.cursor()
  sql = "UPDATE Rates SET rate=%s WHERE product_id = %s AND scope = %s ";

  # sql = "UPDATE Rates SET rate=%s WHERE scope = %s ";
  val = (rate, product_id, scope)
  cursor.execute(sql, val)
  connection.commit()

  print(cursor.lastrowid) 

  return cursor.lastrowid

def get_rate_for_product(connection, provider_id, product):
  cursor = connection.cursor()
  sql = "SELECT * FROM Rates WHERE product_id = %s AND scope = %s;"
  val = (product, get_provider_id_short(provider_id))
  
  cursor.execute(sql, val)
  rate = cursor.fetchone()

  if rate == None:
    sql = "SELECT * FROM Rates WHERE product_id = %s AND scope = 'All';"
    val = (product,)
    
    cursor.execute(sql, val)
    rate = cursor.fetchone()

  return rate[1]

def create_provider(connection, name):
  cursor = connection.cursor()
  sql = "INSERT INTO Provider (id, name) VALUES (%s, %s);"
  val = (None, name)
  cursor.execute(sql, val)
  connection.commit()

  return cursor.lastrowid

def update_provider(connection, id, name):
  cursor = connection.cursor()
  
  sql = "UPDATE Provider SET name = %s WHERE id = %s;"
  val = (name, id)
  cursor.execute(sql, val)
  connection.commit()

  return cursor.lastrowid

def get_truck(connection, number_plate):
  cursor = connection.cursor()

  sql = "SELECT * FROM Trucks WHERE id = %s;"
  val = (number_plate,)
  cursor.execute(sql, val)
  return cursor.fetchone()

def get_truck_for_provider(connection, provider_id):
  cursor = connection.cursor()

  sql = "SELECT * FROM Trucks WHERE provider_id = %s;"
  val = (provider_id,)
  cursor.execute(sql, val)
  return cursor.fetchall()

def create_truck(connection, number_plate, provider_id):
  cursor = connection.cursor()

  sql = "INSERT INTO Trucks (id, provider_id) VALUES (%s, %s);"
  val = (number_plate, provider_id)
  cursor.execute(sql, val)
  connection.commit()

  return number_plate

def update_truck(connection, number_plate, provider_id):
  cursor = connection.cursor()
  
  sql = "UPDATE Trucks SET provider_id = %s WHERE id = %s;"
  val = (provider_id, number_plate)
  cursor.execute(sql, val)
  connection.commit()
  
  return number_plate

def clear_provider_table(connection):
  cursor = connection.cursor()

  sql = "TRUNCATE Provider;"
  cursor.execute(sql)
  connection.commit()

  sql_2 = "ALTER TABLE Provider AUTO_INCREMENT = 10001;"
  cursor.execute(sql_2)
  connection.commit() 