# from unittest import TestCase
# # from backend_config import create_app
# import json

# from flask import Flask
# app = Flask(__name__)


# class TestHome(TestCase):
#     def test_home(self):
#         with app.test_client() as c:
#             response = c.get('/test_route')

#             self.assertEqual(response.status_code, 200)
#             self.assertEqual(json.loads(response.get_data()), {'message': 'Hello, world!'})


# def test_home():
#     with app.test_client() as c:
#         response = c.get('/')

#         assert response.status_code is  200
#         assert json.loads(response.get_data()) == {'message': 'Hello, world!'}