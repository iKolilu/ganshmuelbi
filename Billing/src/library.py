from datetime import datetime

from flask import jsonify, make_response


def make_error(code, message = "an error occurred"):
  return make_response({"error": message}, code)

def make_success(data):
  return make_response(jsonify(data), 200)

def get_date_range(_from, _to) :
  now = datetime.now()
  format = "%Y%m%d%H%M%S"

  # default t1 is "1st of month at 000000". default t2 is "now". 
  date_from = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
  date_to = now

  if _from != None:
    date_from = datetime.strptime(_from, format)
    
  if _to != None:
    date_to = datetime.strptime(_to, format)

  # print(f"date from -> {date_from}")
  # print(f"date to -> {date_to}")

  return {"from": date_from, "to": date_to}
