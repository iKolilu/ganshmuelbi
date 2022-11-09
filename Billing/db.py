import mysql.connector


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
  return "Not implemented"


def get_one_rate(product_id, scope):
  sql = "SELECT * FROM Rates WHERE product_id = %s AND scope = %s;"
  val = (product_id, scope)

  mycursor.execute(sql, val)
  myresult = mycursor.fetchall()

  print(myresult)
  return myresult  

def get_all_rates(product_id):
  sql = "SELECT * FROM Rates;"

  mycursor.execute(sql)
  myresult = mycursor.fetchall()

  print(myresult)
  return myresult


def create_rates(product_id, rate, scope):
  sql = "INSERT INTO Rates (product_id, rate, scope) VALUES (%s, %s, %s);"
  val = (product_id, rate, scope)
  mycursor.execute(sql, val)
  mydb.commit()

  print(mycursor.lastrowid)

  return mycursor.lastrowid



def update_rates_same_pid_scope(product_id, rate, scope):
  sql = "UPDATE Rates SET rate=%s WHERE product_id = %s AND scope = %s ";

  # sql = "UPDATE Rates SET rate=%s WHERE scope = %s ";
  val = (rate, product_id, scope)
  mycursor.execute(sql, val)
  mydb.commit()

  print(mycursor.lastrowid) 

  return mycursor.lastrowid



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
