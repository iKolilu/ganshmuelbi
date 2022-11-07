from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
  return "Welcome to the Gan Shmuel Billing"


@app.route("/provider", methods=["POST"])
def provider_create():
  return "Not implemented"

@app.route("/provider", methods=["PUT"])
def provider_update():
  return "Not implemented"

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
  return "Not implemented"

if __name__ == '__main__':
  app.run()