from datetime import datetime

from flask import jsonify, make_response


def make_error(code, message = "an error occurred"):
  return make_response({"error": message}, code)



def make_success(data):
  return make_response(jsonify(data), 200)



def get_date_format_text(date) :
  format = "%Y%m%d%H%M%S"
  return datetime.strftime(date, format)


def get_date_range(_from, _to) :
  now = datetime.now()
  format = "%Y%m%d%H%M%S"
  # yyyymmddhhmmss

  # default t1 is "1st of month at 000000". default t2 is "now". 
  date_from = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
  date_to = now

  if _from != None:
    date_from = datetime.strptime(_from, format)
    
  if _to != None:
    date_to = datetime.strptime(_to, format)

  return {"from": date_from, "to": date_to}



def get_provider_id_long(int_provider_id):
  return int(int_provider_id) + 10000



def get_provider_id_short(str_provider_id):
  val = int(str_provider_id) - 10000
  if val > 0:
    return val
  return int(str_provider_id)