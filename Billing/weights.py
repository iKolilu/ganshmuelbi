import os

import requests
from library import get_date_format_text


def weight_address():
  return os.environ['WEIGHT_ADDRESS']

def get_item(id, date_range):
  host = weight_address()

  r = requests.get(f"{host}/item/{id}", params={
    "from": get_date_format_text(date_range['from']),
    "to": get_date_format_text(date_range['to']),
  })
  print(f"r -> {r}")
  
  if r.status_code == 404:
    raise Exception(f'Weight server: Truck data not found for ID {id}')
  elif r.status_code != 200:
    raise Exception(f'Weight server: {r.status_code} error')

  return r.json()
  

def get_weight(date_range):
  host = weight_address()

  r = requests.get(f"{host}/weight", params={
    "from": get_date_format_text(date_range['from']),
    "to": get_date_format_text(date_range['to']),
    "filter": "out",
  })
  print(f"r -> {r}")
  
  if r.status_code == 404:
    raise Exception('Weight server: Weight sessions not found')
  elif r.status_code != 200:
    raise Exception('Weight server: error')

  return r.json()

def get_session(id):
  host = weight_address()

  r = requests.get(f"{host}/session/{id}")
  print(f"r -> {r}")
  
  if r.status_code == 404:
    raise Exception('Weight server: Session ID not found')
  elif r.status_code != 200:
    raise Exception('Weight server: error')

  return r.json()