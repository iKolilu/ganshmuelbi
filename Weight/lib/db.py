import mysql.connector
from datetime import datetime


class db:
    def __init__(self, host, port, username, password, database):
        self.db = mysql.connector.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            database=database
        )
        self.db_cursor = self.db.cursor()

    def show_tables(self):
        self.db_cursor.execute('SHOW TABLES')
        for i in self.db_cursor:
            print(i)
        return 'success'

    def create_table(self, table_name, parameters_string):
        pass

    def add_truck_in(self, truck, containers, direction, bruto, produce, neto=None, truckTara=None):
        now = datetime.now().strftime('%Y%m%d%H%M%S')
        if neto == None:
            neto = 'null'
        if truckTara == None:
            truckTara = 'null'
        # print(now)
        self.db_cursor.execute(
            f"INSERT INTO transactions(datetime, direction, truck, containers, bruto, truckTara, neto, produce) values('{now}', '{direction}', '{truck}', '{containers}', {bruto}, {truckTara}, {neto}, '{produce}')"
        )
        self.db.commit()
        return {
            'id': self.db_cursor.lastrowid,
            'truck': truck,
            'bruto': bruto}

    def check_last_direction_of_truck(self, truck_license):
        self.db_cursor.execute(
            f"SELECT * FROM transactions WHERE truck = '{truck_license}' ORDER BY datetime DESC LIMIT 1")
        # for i in self.db_cursor:
        #     print(i)
        transactify = [i for i in self.db_cursor][0]
        transactify = self.transaction_objectify(transactify)
        return transactify

    def overwite_previous_truck_in_in(self, old_data, new_truck_weight):
        # try:
        #     diff = new_truck_weight - old_data['truckTara']
        # except Exception as e:
        #     print(e)
        #     new_truck_weight = new_truck_weight
        new_bruto = new_truck_weight

        # self.db_cursor.execute(
        #     f"INSERT INTO transactions(id, datetime, direction, truck, containers, bruto, truckTara, neto, produce) values({old_data['id']}, '{old_data['datetime']}', '{old_data['direction']}', '{old_data['truck']}', '{old_data['containers']}', {new_bruto}, {new_truck_weight}, {old_data['neto']}, '{old_data['produce']}')"
        # )
        # self.db_cursor.execute(
        #     f"SELECT bruto, truckTara FROM transactions WHERE id = {old_data['id']}")
        self.db_cursor.execute(
            f"UPDATE transactions SET bruto = {new_bruto} WHERE id = {old_data['id']}"
        )
        self.db.commit()

        updated = self.check_last_direction_of_truck(old_data['truck'])
        return {
            'id': updated['id'],
            'truck': updated['truck'],
            'bruto': updated['bruto']
        }

    def none_handle_container(self, c_id, weight, unit):
        if not self.does_container_exists(c_id):
            added = self.none_add_container(c_id, weight, unit)
            return added
        else:
            added = self.none_update_container(c_id, weight, unit)
            return added

    def none_add_container(self, c_id, weight, unit):
        self.db_cursor.execute(
            f"INSERT INTO containers_registered(container_id, weight, unit) values('{c_id}', {weight}, '{unit}')"
        )

        self.db.commit()

        return {
            'message': 'success',
            'data': {
                'container_id': c_id,
                'weight': weight,
                'unit': unit,
            }
        }

    def none_update_container(self, c_id, weight, unit):
        self.db_cursor.execute(
            f"UPDATE containers_registered SET weight = {weight}, unit = '{unit}' WHERE container_id = '{c_id}'"
        )
        self.db.commit()

        return {
            'message': 'success',
            'data': {
                'container_id': c_id,
                'weight': weight,
                'unit': unit,
            }
        }

    def transaction_objectify(self, transaction, flag=None):
        #print(transaction[0], transaction[1], transaction[2])
        if flag == None:
            return {
                'id': transaction[0],
                'datetime': transaction[1],
                'direction': transaction[2],
                'truck': transaction[3],
                'containers': transaction[4],
                'bruto': transaction[5],
                'truckTara': transaction[6],
                'neto': transaction[7],
                'produce': transaction[8]
            }

    def does_truck_exist_in_db(self, truck):
        self.db_cursor.execute(
            f"SELECT id FROM transactions WHERE truck = '{truck}'"
        )

        rows = self.db_cursor.fetchall()

        if len(rows) > 0:
            return True
        return False

    def does_container_exists(self, cont_id):
        self.db_cursor.execute(
            f"SELECT * FROM containers_registered WHERE container_id = '{cont_id}'"
        )
        rows = self.db_cursor.fetchall()

        if len(rows) > 0:
            return True
        return False

    def out_update_truckTara(self, old_data, weight, direction):
        self.db_cursor.execute(
            f"UPDATE transactions SET truckTara = {weight}, direction = '{direction}' WHERE id = {old_data['id']}"
        )
        self.db.commit()
        updated = self.check_last_direction_of_truck(old_data['truck'])
        return {
            'id': updated['id'],
            'truck': updated['truck'],
            'bruto': updated['bruto'],
            'truckTara': updated['truckTara'],
            'neto': updated['neto']
        }

    def get_truck_weights(self, from_, to_, f_):
        status_code = 200
        message = ''
        if from_ == None or from_ == '':
            todays_date = datetime.now().strftime('%Y%m%d000000')
            from_ = todays_date
        else:
            from_ = datetime.strptime(from_, '%Y%m%d%H%M%S')
        if to_ == None or to_ == '':
            to_ = datetime.now().strftime('%Y%m%d%H%M%S')
        else:
            to_ = datetime.strptime(to_, '%Y%m%d%H%M%S')
        if f_ == None or f_ == '':
            f_ = 'in,out,none'

        out_already = self.db_cursor.execute(
            "SELECT * FROM transactions WHERE truckTara is Null")
        #"SELECT * FROM transactions WHERE neto is Null OR truckTara is Null"
        rows = self.db_cursor.fetchall()
        # print(rows)
        if len(rows) > 0:
            status_code = 206
            message = 'Some trucks are not out yet, please wait ...'

        neto_already = self.db_cursor.execute(
            "SELECT * FROM transactions WHERE neto is Null")
        rows = self.db_cursor.fetchall()
        # print(rows)
        if len(rows) > 0:
            status_code = 206
            message = message + '\nMake Sure to calculate all neto before using data ...'

        f_final = f_.split(',')
        f_query_string = ''
        for idx, el in enumerate(f_final):
            if idx == 0:
                f_query_string = f"(containers LIKE '%{el}%')"
            else:
                f_query_string = f_query_string + \
                    f" OR (containers LIKE '%{el}%')"
        f_query_string = "(" + f_query_string + ")"

        self.db_cursor.execute(
            f"SELECT * FROM transactions WHERE (datetime > '{from_}' AND datetime < '{to_}') AND {f_query_string}")
        rows = self.db_cursor.fetchall()
#            print('WEIGHTS', rows)
        results = [self.transaction_objectify(i) for i in rows]
        # results['']
        return [results, status_code, message]

#         if len(f_final) == 3:
#             self.db_cursor.execute(
#                 f"SELECT * FROM transactions WHERE (datetime > '{from_}' AND datetime < '{to_}') AND ((containers LIKE '%{f_final[0]}%') OR (containers LIKE '%{f_final[1]}%') OR (containers LIKE '%{f_final[2]}%'))")
#             rows = self.db_cursor.fetchall()
# #            print('WEIGHTS', rows)
#             results = [self.transaction_objectify(i) for i in rows]
#             return results

#         elif len(f_final) == 2:
#             self.db_cursor.execute(
#                 f"SELECT * FROM transactions WHERE (datetime > '{from_}' AND datetime < '{to_}') AND ((containers LIKE '%{f_final[0]}%') OR (containers LIKE '%{f_final[1]}%'))")
#             rows = self.db_cursor.fetchall()
# #            print('WEIGHTS', rows)
#             results = [self.transaction_objectify(i) for i in rows]
#             return results
#         elif len(f_final) == 1:
#             self.db_cursor.execute(
#                 f"SELECT * FROM transactions WHERE (datetime > '{from_}' AND datetime < '{to_}') AND (containers LIKE '%{f_final[0]}%')")
#             rows = self.db_cursor.fetchall()
# #            print('WEIGHTS', rows)
#             results = [self.transaction_objectify(i) for i in rows]
#             return results

    def get_container_weights(self, from_, to_, f_):
        f_query_string = ""

        for idx, el in enumerate(f_.split(',')):
            if idx == 0:
                f_query_string = f_query_string + \
                    f"(container_id LIKE '%{el}%')"
            else:
                f_query_string = f_query_string + \
                    f" OR (container_id LIKE '%{el}%')"

        # f_query_string = "(" + f_
        if len(f_query_string) > 0:
            f_query_string = " WHERE " + f_query_string

        self.db_cursor.execute(
            f"SELECT * FROM containers_registered{f_query_string}")
        rows = self.db_cursor.fetchall()
#            print('WEIGHTS', rows)
        results = [{
            'id': i[0],
            'weight':i[1],
            'unit':i[2]
        } for i in rows]
        # results['']
        print(results)
        return results
