

import db
from flask import Flask, jsonify, make_response, render_template, request, send_file
from library import get_date_range, make_error, make_success
from remote import get_item_from_weights

from werkzeug.utils import secure_filename

import os
import openpyxl

import csv
app = Flask(__name__)


@app.route("/")
def home():
  return render_template("index.html")

@app.route("/test_route")
def test_route():
  return jsonify({'message': 'Hello, world!'})

@app.route("/provider", methods=["POST"])
def provider_create():
  new_name = request.json.get('name')
  provider_id = db.create_provider(database, new_name)
  return make_success({"id": provider_id})

@app.route("/provider/<id>", methods=["PUT"])
def provider_update(id):
  new_name = request.json.get('name')
  db.update_provider(database, id, new_name)
  return make_success({"id": id, "name": new_name})



@app.route("/rates", methods=["GET"])
def rates_get():

  
  dir_name = os.path.join("in", 'rates.xlsx')

  return send_file(dir_name, mimetype='xlsx')



@app.route("/rates", methods=["POST"])
def rates_create():
  database = db.connect()
  try:      
    dataframe = openpyxl.load_workbook("in/rates.xlsx")
    dataframe1 = dataframe.active
    
    testArray = []
    # Iterate the loop to read the cell values
    for row in range(1, dataframe1.max_row):
      
      testDict={}
      for col in dataframe1.iter_cols(1, dataframe1.max_column):
        
        if col[0].value == "Scope":
          testDict[col[0].value] = str(col[row].value)
        elif col[0].value == "Product":
          testDict[col[0].value] = str(col[row].value)    
        else:
          testDict[col[0].value] = int( col[row].value )

      testArray.append(testDict)  
    
    for x in testArray:

      if db.get_one_rate(x["Product"], x["Scope"]) != []:
        print(x, "found one ===> ")
        db.update_rates_same_pid_scope(x["Product"], x["Rate"], x["Scope"])
      else:
        db.create_rates(x["Product"], x["Rate"], x["Scope"])

    return jsonify({"status_code": 200, "success": "true"})

  except:
    return jsonify({"status_code": 400, "success": "false"})    
  
    


@app.route("/truck", methods=["POST"])
def truck_create():
  number_plate = request.json.get('number_plate')
  provider_id = request.json.get('provider_id')
  truck = db.create_truck(database, number_plate, provider_id)
  return make_success({"id": truck})

@app.route("/truck/<id>", methods=["PUT"])
def truck_update(id):
  provider_id = request.json.get('provider_id')
  
  truck = db.update_truck(database, id, provider_id)
  
  return make_success({"id": truck, "provider_id": provider_id})

@app.route("/truck/<id>", methods=["GET"])
def truck_get(id):
  _from = request.args.get('from')
  _to = request.args.get('to')
  
  dates = get_date_range(_from, _to)

  # check db first
  truck = db.get_truck(database, id)

  if not truck:
    return make_error(404, 'not found')

  truck_data = get_item_from_weights(id, dates)

  if not truck_data:
    return make_error(404, 'not found')

  return make_success(truck_data)

@app.route("/bill/<id>", methods=["GET"])
def bill_get(id):
  return "Not implemented"

@app.route("/health", methods=["GET"])
def health():
  if db.connect() != None:
    return make_response("OK", 200)
    
  return make_response("Failure", 500)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
