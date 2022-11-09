import db
from flask import Flask, jsonify, make_response, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
  return "Welcome to the Gan Shmuel Billing"

@app.route("/provider", methods=["POST"])
def provider_create():
  new_name = request.json.get('name')
  provider_id = db.create_provider(new_name)
  return jsonify({"id": provider_id})

@app.route("/provider/<id>", methods=["PUT"])
def provider_update(id):
  new_name = request.json.get('name')
  db.update_provider(id, new_name)
  return jsonify({"id": id, "name": new_name})

@app.route("/rates", methods=["GET"])
def rates_get():
  return "Not implemented"

@app.route("/rates", methods=["POST"])
def rates_create():
  return "Not implemented"
    
@app.route("/truck", methods=["POST"])
def truck_create():
  return "Not implemented"

@app.route("/truck/<id>", methods=["PUT"])
def truck_update(id):
  return "Not implemented"

@app.route("/truck/<id>", methods=["GET"])
def truck_get(id):
  return "Not implemented"

@app.route("/bill/<id>", methods=["GET"])
def bill_get(id):
  return "Not implemented"

@app.route("/health", methods=["GET"])
def health():
  if db.connect():
    return make_response("OK", 200)
    
  return make_response("Failure", 500)

if __name__ == '__main__':
  app.run()