from flask import Flask, jsonify, abort, request, render_template, redirect, url_for, flash
import os
import json
import csv

app = Flask('__main__', template_folder='templates')


# mydb = mysql.connector.connect(
#     host="localhost",
#     user="crommie",
#     password="123@admin"
# )

# sesssion_record = [
#     {"id": "1",
#      "truck": "GT-2852-11",
#      "bruto": 45.4,
#      "truckTara": 45.12,
#      "neto": 40.1
#      },
#     {"id": "2",
#      "truck": "CR-116-17",
#      "bruto": 80,
#      "truckTara": 70,
#      "neto": 65
#      },
#     {"id": "3",
#      "truck": "GT-15-U",
#      "bruto": 20,
#      "truckTara": 18,
#      "neto": 15
#      }
# ]


@app.errorhandler(404)
def resouce_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource Not Found"
    })


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal Server Error"
    })


@ app.route("/")
def home():
    # return "Welcome to the Gan Shmuel Weight"
    return render_template("file_upload_form.html")


@ app.route("/weigth", methods=["GET", "POST"])
def weight():
    return "Not implemented"


@app.route("/batch-weight", methods=["POST"])
def batch_weight():
    body = request.get_json()
    weight_data = []
    file_name = body['file']
    type_of_file = body['type']

    if os.path.exists(f"/in/{file_name}"):
        print("file exist")
        with open(f"/in/{file_name}", "r") as file:
            if type_of_file.lower() == "json":
                data_weight = json.load(file)

                for row in data_weight:
                    id = row['id']
                    unit = row['unit']
                    weight = row['weight']

                    weight_data.append({
                        "id": id,
                        "unit": unit,
                        "weight": weight,
                    })

            elif type_of_file.lower() == "csv":

                reader = csv.DictReader(file)
                for row in reader:
                    id = row['id']
                    unit = "kg"
                    weight = row['kg']

                    # query_statement = f"INSERT INTO (id, unit, weight) VALUES({id},{unit},{weight})"
                    # cursor.execute(query_statement)

                    weight_data.append({
                        "id": id,
                        "unit": unit,
                        "weight": weight,
                    })

    return jsonify({
        "weight_data": weight_data
    })


@app.route("/unknown", methods=["GET"])
def unknown():
    return "Not implemented"


@app.route("/item/<id>", methods=["GET"])
def item(id):
    return "Not implemented"


<< << << < HEAD


@ app.route("/session")
@ app.route("/session/<id>")
def session(id=None):
    try:
        if id:
            for data in sesssion_record:
                if data["id"] == str(id):
                    return jsonify(data)
            abort(404)
        else:
            return jsonify(sesssion_record)
    except Exception as err:
        abort(500)


@ app.route("/health", methods=["GET"])
def health():
   if db.engine.execute('SELECT 1'):
        return make_response("OK", 200)
    else:
        return make_response("Failure", 500)



if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0', port=7007)
