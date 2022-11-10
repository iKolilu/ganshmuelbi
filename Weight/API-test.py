#!/usr/bin/env python3

import requests
import json

url = "http://0.0.0.0:3000/health/"

payload = json.dumps({
    "file": "containers2.csv"
})
headers = {
    'Content-Type': 'application/json'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
