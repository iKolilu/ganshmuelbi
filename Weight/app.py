from flask import Flask, render_template, request, Response, jsonify
from lib.db import db

base = db(
    host='localhost', port=8877,
    username='root', password='password',
    database='weight'
)


app = Flask('__main__', template_folder='templates')


@app.route("/")
def home():
    return "Welcome to the Gan Shmuel Weight"


@app.route("/weight/<id>/", methods=["GET"])
def get_weight(id):
    print(id)
    from_ = request.args.get('from')
    to_ = request.args.get('to')
    f_ = request.args.get('filter')

    initials = id.split('-')[0]
    print(initials)
    retrieval = []
    if initials.lower() == 't' or initials.lower() == 'k':
        print('truck')
        retrieval = base.get_truck_weights(from_=from_, to_=to_, f_=f_)
        if retrieval[1] == 200:
            return jsonify(
                {
                    'data': retrieval[0]
                    # TODO sessions
                }
            )
        else:
            return jsonify(
                {
                    'data': retrieval[0],
                    'warning': retrieval[2]
                    # TODO sessions
                }
            ), retrieval[1]
    elif initials.lower() == 'c':
        conts = base.get_container_weights(from_=None, to_=None, f_=f_)
        return jsonify(conts), 200
    return Response('error', 200)


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
    return "Not implemented"


@app.route("/unknown", methods=["GET"])
def unknown():
    return "Not implemented"


@app.route("/item/<id>", methods=["GET"])
def item(id):
    return "Not implemented"


@app.route("/session/<id>", methods=["GET"])
def session(id):
    return "Not implemented"


@app.route("/health", methods=["GET"])
def health():
    return "Not implemented"


if __name__ == '__main__':
    app.run(debug=True)
