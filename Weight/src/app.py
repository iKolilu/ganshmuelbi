#!/usr/bin/env python3

from flask import Flask, render_template, request, Response, jsonify, abort, redirect, url_for, flash
from lib.db import db
import os
import mimetypes as mt
import pandas as pd

base = db(
    host='mysqldb', port=3306,
    username='root', password='123@admin',
    database='weight'
)

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
    return "Welcome to the Gan Shmuel Weight"


@app.route("/weight/", methods=["GET"])
def get_weight():
    # print(id)
    from_ = request.args.get('from')
    to_ = request.args.get('to')
    f_ = request.args.get('filter')

    # initials = id.split('-')[0]
    # print(initials)
    # retrieval = []
    # if initials.lower() == 't' or initials.lower() == 'k' or initials.lower() == 'c':
    #     #print('truck')
    retrieval = base.get_truck_weights(from_=from_, to_=to_, f_=f_)
    if retrieval[1] == 200:
        return jsonify(retrieval[0])
        # jsonify(
        #     {
        #         'data': retrieval[0]
        #         # TODO sessions
        #     }
        # )
    else:
        return jsonify(retrieval[0])
        # return jsonify(
        #     {
        #         'data': retrieval[0],
        #         'warning': retrieval[2]
        #         # TODO sessions
        #     }
        # ), retrieval[1]
    # elif initials.lower() == 'c':
    #     conts = base.get_container_weights(from_=None, to_=None, f_=f_)
    #     return jsonify(conts), 200
    # else:
    #     abort(Respo)
    return Response('error', 400)


@app.route('/weight/', methods=["POST"])
def weight():
    args = request.get_json()
    direction = args['direction'].lower()
    try:
        truck = args['truck']
        if truck == None or truck == '':
            truck = 'na'
    except:
        pass
    try:
        containers = args['containers']
    except:
        pass

    weight = args['weight']
    try:
        unit = args['unit']
    except:
        pass
    try:
        force = args['force']
    except:
        pass
    try:
        produce = args['produce']
    except:
        pass

    # DIRECTIONS
    if direction == 'in':
        # TODO
        exists = base.does_truck_exist_in_db(truck)
        if not exists:
            # add to db
            added = base.add_truck_in(
                truck=truck, containers=containers, direction=direction, bruto=weight, produce=produce)
            return jsonify(added)

        last_movement = base.check_last_direction_of_truck(truck_license=truck)

        if last_movement['direction'].lower() == 'out':
            # go ahead and add to db
            added = base.add_truck_in(
                truck=truck, containers=containers, direction=direction, bruto=weight, produce=produce)
            return jsonify(added)
        elif last_movement['direction'].lower() == 'in':
            if force == True:
                # overide
                overwrite = base.overwite_previous_truck_in_in(
                    old_data=last_movement, new_truck_weight=weight)
                return jsonify(overwrite)
            else:
                return Response('error', 400)

    elif direction == 'out':
        # check for existence
        exists = base.does_truck_exist_in_db(truck)
        if not exists:
            return Response('error', 406)

        # TODO
        last_movement = base.check_last_direction_of_truck(
            truck_license=truck)
        if last_movement['direction'].lower() == 'in':
            # TODO proceed out
            procees = base.out_update_truckTara(
                old_data=last_movement, weight=weight, direction=direction)
            return jsonify(procees)
        elif last_movement['direction'] == 'out':
            # check force
            if force == True:
                # overwitee
                overwrite = base.out_update_truckTara(
                    old_data=last_movement, weight=weight, direction=direction)
                return jsonify(overwrite)
            else:
                return Response('error', 400)

        pass
    elif direction == 'none':
        results = base.none_handle_container(
            c_id=containers, weight=weight, unit=unit)
        return results

    else:
        return Response('error', 400)


@app.route("/batch-weight/", methods=["POST"])
def batch_weight():
    args = request.get_json()
    filename = args['file']
    path = f'/in/{filename}'
    path = os.path.normpath(path)
    df = None
    multiplier = 1.0
    columns = {
        'id': 'id'
    }

    if filename == None or filename == '':
        abort(Response('Provide valide file', 400))

    if not (os.path.exists(path) and os.path.isfile(path)):
        abort(Response('Provide valide file', 400))

    if mt.guess_type(path)[0] == 'application/json':
        df = pd.read_json(path)
        columns['weight'] = 'weight'
        if df['unit'].loc[0] == 'lbs':
            multiplier = 0.453592

        results = base.batch_weight_handler(df, columns, multiplier)
        return jsonify(results), 200

    elif mt.guess_type(path)[0] == 'text/csv':
        df = pd.read_csv(path)
        columns['weight'] = df.columns[1]
        if df.columns[1] == 'lbs':
            multiplier = 0.453592

        results = base.batch_weight_handler(df, columns, multiplier)
        return jsonify(results), 200
    else:
        abort(Response('Provide valide file', 400))


@app.route("/unknown/", methods=["GET"])
def unknown():
    # Returns a list of all recorded containers that have unknown weight
    unknowns = base.get_unknowns()
    return jsonify(unknowns), 200


@app.route("/item/<id>/", methods=["GET"])
def item(id):
    from_ = request.args.get('from')
    to_ = request.args.get('to')

    try:
        T_or_C = id.split('-')[0].lower()
    except:
        return Response('error', 400)

    # if T_or_C == 't' or T_or_C == 'k':
        # truck stuff
    exists = base.does_truck_or_container_exist_in_db(id)
    if not exists:
        return Response('resource not available', 404)

    results = base.get_item_truck(id, from_=from_, to_=to_)
    if results == []:
        results = base.get_item_container(id, from_, to_)
        if results == []:
            return Response('resource not available', 404)
    return jsonify(results)
    # else:
    #     exists = base.does_truck_exist_in_db(
    #         id) or base.does_container_exists_in_transactions(id)
    #     if not exists:
    #         return Response('resource not available', 404)
    #     results = base.get_item_container(id, from_, to_)
    #     if results == []:
    #         return Response('resource not available', 404)
    #     return jsonify(results)

    # container stuff


@app.route("/session/<id>/", methods=["GET"])
def session(id):

    exists = base.session_exists(id)
    if not exists:
        return Response('session not available', 404)
    results = base.get_session(id)
    return jsonify(results)


@app.route("/health/", methods=["GET"])
def health():
    return Response('Okay', 200)


if __name__ == '__main__':
    app.run(port=9090, host="0.0.0.0", debug=True)
