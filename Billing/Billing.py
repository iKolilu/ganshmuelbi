

import db
from flask import Flask, jsonify, make_response, render_template, request
from library import get_date_range, make_error, make_success
from remote import get_item_from_weights

import csv
app = Flask(__name__)
database = db.connect()

@app.route("/")
def home():
  return "Welcome to the Gan Shmuel Billing"

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
  return "Not implemented"



@app.route("/rates", methods=["POST"])
def rates_create():

  # new_rate = request.json.get('rate')
  # rate_id = db.create_provider(new_rate)

  # new_rate = db.update_rates_same_pid_scope("late", 45, "All")

  # new_rate = db.create_rates("lat", 21, "All")

  # new_rate = db.get_one_rate("lat", "Alx")

  
  newDict = [
    {"product_id": "lat", "rate": 21, "scope": "All"},
    {"product_id": "late","rate": 45, "scope": "All"},
    { "product_id": "only","rate": 47,"scope": "45"}
  ]

  count = 0

  # first check if it exists db.get_one_rate("lat", "Alx") ,  empty [] means does not exists
  # if no then db.create_rates, or 
  # else  db.update_rates_same_pid_scope("late", 45, "All")

  new_rate=""
  for x in newDict:
    count = count + 1
    print(x, count)

    if db.get_one_rate(x["product_id"], x["scope"]):
      print(x, "found one ===> ")
      new_rate = db.update_rates_same_pid_scope(x["product_id"], x["rate"], x["scope"])
    else:
      new_rate = db.create_rates(x["product_id"], x["rate"], x["scope"])


  return jsonify({"id": "32", "name": new_rate})
  
    
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
  app.run(debug=True, host='0.0.0.0', port=4000)
