from flask import Flask,render_template


app = Flask('__main__',template_folder='templates')

@app.route("/")
def home():
    return "Welcome to the Gan Shmuel"


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)
