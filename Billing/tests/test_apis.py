import pytest

from .conftests import *

def test_mock_route(client):
    rv = client.get("/mock_routeK")


    print("##### Begin Testing the apis status code######")

    assert rv.status_code is 200 , f" 200 status_code if successful expected, got something else"


    print("##### Ended Testing the apis status code######")
    print("#################################################")
    print("#################################################")



def test_mock_route_return_value(client):
    rv = client.get("/mock_route")

    print("##### Started Testing the return ######")

    assert b"Hello World" == rv.data, f" 'Hello World' return statement if successful expected, got something else"

    print("##### Ended Testing the apis status code######") 


