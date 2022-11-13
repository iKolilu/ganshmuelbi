
import pytest, time

from .conftests import *
from flask import json
from db import  get_provider, create_provider, connect, clear_provider_table, clear_a_record_provider_table
connection=connect()







def test_mock_route(client):
    rv = client.get("/")
    

    print("##### Begin Testing the apis status code######")

    assert rv.status_code is  200 , f" 200 status_code  if successful expected, got something else"
    

    print("##### Ended Testing the apis status code######")
    print("#################################################")
    print("#################################################")



def test_mock_route_return_value(client):
    rv = client.get("/")


    print("##### Started Testing the return  ######")

    assert b"Welcome to GanShmuel Billing Server" == rv.data, f" 'Welcome to GanShmuel Billing Server' return statement  if successful expected, got something else"

    print("##### Ended Testing the apis status code######")




    



    


def test_post_provider_value(client):

    clear_a_record_provider_table(connection)

    rv = client.post('/provider', json={
        'name': 'kwameJude'}, content_type='application/json')

    assert rv.status_code is 200 , f" 200 status_code  if successful expected, got something else"

    json_data = rv.data
    # my_res_data =  json.dumps({'id': 10001})

    time.sleep(2)

    assert b'10001' in json_data


def test_health(client):

    rv = client.get('/health')

    print("#####  Testing the healtapis status code######")
    # time.sleep(1)
    assert rv.status_code is 200 , f" 200 status_code  if successful expected, got something else"
    print("#####  Done testing the health apis status code######")


    







