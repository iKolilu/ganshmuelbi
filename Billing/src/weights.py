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
    raise Exception('truck not found')
  elif r.status_code != 200:
    raise Exception('weight server error')

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
    raise Exception('weight not found')
  elif r.status_code != 200:
    raise Exception('weight server error')

  return r.json()

  # f = out
  mock = { 
    "id": 'asdf1',
    "direction": "out",
    "bruto": 603,
    "neto": 234,
    "produce": "Grapefruit",
    "containers": [ "asdf1", "asdf2", "asdf3" ],
  }
  mock2 = { 
    "id": 'asdf3',
    "direction": "out",
    "bruto": 603,
    "neto": 234,
    "produce": "Grapefruit",
    "containers": [ "asdf1", "asdf2", "asdf3" ],
  }
  return [mock, mock2]