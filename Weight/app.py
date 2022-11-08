from flask import Flask, render_template, request


app = Flask('__main__', template_folder='templates')


@app.route("/")
def home():
    return "Welcome to the Gan Shmuel Weight"


@app.route("/weigth", methods=["GET", "POST"])
def weight():
    return "Not implemented"


@app.route("/batch-weight", methods="POST")
def batch_weight():
    return "Not implemented"


@app.route("/unknown", methods="GET")
def unknown():
    return "Not implemented"


@app.route("/item/<id>", methods="GET")
def item(id):
    return "Not implemented"


@app.route("/session/<id>", methods="GET")
def session(id):
    return "Not implemented"


@app.route("/health", methods="GET")
def health():
    if db.engine.execute('SELECT 1'):
        return make_response("OK", 200)
    else:
        return make_response("Failure", 500)


if __name__ == '__main__':
    app.run(debug=True)
