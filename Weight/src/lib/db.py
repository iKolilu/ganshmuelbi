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

    def add_truck_in(self, truck, containers, direction, bruto, produce, neto=None, truckTara=None):
        now = datetime.now().strftime('%Y%m%d%H%M%S')
        if neto == None or neto == '':
            neto = 'null'
        if truckTara == None or truckTara == '':
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
        self.db_cursor.execute(
            f"insert into transactions(datetime, direction, truck, containers, bruto, truckTara, neto, produce) values('{datetime.now().strftime('%Y%m%d%H%M%S')}', 'none', NULL, '{c_id}',NULL, NULL, NULL, NULL, NULL);"
        )

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

    def does_truck_or_container_exist_in_db(self, id):
        self.db_cursor.execute(
            f"SELECT id FROM transactions WHERE (truck = '{id}') OR (containers LIKE '%{id}%')"
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

    def does_container_exists_in_transactions(self, cont_id):
        self.db_cursor.execute(
            f"SELECT * FROM transactions WHERE containers LIKE '%{cont_id}%'"
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

        f_final = f_.split(',')
        f_query_string = ''
        for idx, el in enumerate(f_final):
            if idx == 0:
                f_query_string = f"(direction LIKE '%{el}%')"
            else:
                f_query_string = f_query_string + \
                    f" OR (direction LIKE '%{el}%')"
        f_query_string = "(" + f_query_string + ")"
        f_query_string = f" AND {f_query_string}"

        #print(f_, f_final, f_query_string)

        try:
            if f_ == None or f_ == '':
                f_query_string = ''
        except:
            pass

        out_already = self.db_cursor.execute(
            f"SELECT * FROM transactions WHERE truckTara is Null AND (datetime > '{from_}' AND datetime < '{to_}'){f_query_string}")
        #"SELECT * FROM transactions WHERE neto is Null OR truckTara is Null"
        rows = self.db_cursor.fetchall()
        # print(rows)
        if len(rows) > 0:
            status_code = 206
            message = 'Some trucks are not out yet, please wait ...'

        neto_already = self.db_cursor.execute(
            f"SELECT * FROM transactions WHERE neto is Null AND (datetime > '{from_}' AND datetime < '{to_}'){f_query_string}")
        rows = self.db_cursor.fetchall()
        # print(rows)
        if len(rows) > 0:
            status_code = 206
            message = message + '\nMake Sure to calculate all neto before using data ...'

        self.db_cursor.execute(
            f"SELECT * FROM transactions WHERE (datetime > '{from_}' AND datetime < '{to_}'){f_query_string}")
        rows = self.db_cursor.fetchall()
#            print('WEIGHTS', rows)
        results = [self.transaction_objectify(i) for i in rows]
        # results['']
        return [[self.format_get_weight(i) for i in results], status_code, message]

    def format_get_weight(self, res):
        # print(res)
        return {
            'id': res['id'],
            'direction': res['direction'],
            'bruto': res['bruto'],
            'neto': res['neto'],
            'produce': res['produce'],
            'containers': res['containers'].split(",")
        }

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

    def get_unknowns(self):
        self.db_cursor.execute(
            f"SELECT container_id FROM containers_registered WHERE weight IS NULL"
        )
        rows = self.db_cursor.fetchall()
        print(rows)

        return [i[0] for i in rows]

    def get_item_truck(self, id, from_, to_):
        if from_ == None or from_ == '':
            date_today = datetime.now()
            from_ = date_today.replace(
                day=1, hour=0, minute=0, second=0, microsecond=0).strftime('%Y%m%d%H%M%S')
        else:
            from_ = datetime.strptime(from_, '%Y%m%d%H%M%S')
        if to_ == None or to_ == '':
            to_ = datetime.now().strftime('%Y%m%d%H%M%S')
        else:
            to_ = datetime.strptime(to_, '%Y%m%d%H%M%S')

        last_known_tara = self.last_known_tara(id, from_, to_)
        if last_known_tara == 'na':
            return []
        truck_sesions = self.get_item_truck_sessions(id, from_, to_)
        if truck_sesions == []:
            return []

        return {
            'id': id,
            'tara': last_known_tara,
            'sessions': truck_sesions
        }

    def get_item_truck_sessions(self, id, from_, to_):
        self.db_cursor.execute(
            f"SELECT id FROM transactions WHERE (truck = '{id}') AND (datetime > '{from_}' AND datetime < '{to_}')"
        )
        rows = self.db_cursor.fetchall()

        return [i[0] for i in rows]

    def last_known_tara(self, id, from_, to_):
        self.db_cursor.execute(
            f"SELECT truckTara FROM transactions WHERE (truck = '{id}') AND (datetime > '{from_}' AND datetime < '{to_}') ORDER BY id DESC LIMIT 1"
        )
        row = self.db_cursor.fetchall()
        if not len(row) > 0:
            row = ['na']
        return row[0]

    def get_item_container(self, id, from_, to_):
        if from_ == None or from_ == '':
            date_today = datetime.now()
            from_ = date_today.replace(
                day=1, hour=0, minute=0, second=0, microsecond=0).strftime('%Y%m%d%H%M%S')
        else:
            from_ = datetime.strptime(from_, '%Y%m%d%H%M%S')
        if to_ == None or to_ == '':
            to_ = datetime.now().strftime('%Y%m%d%H%M%S')
        else:
            to_ = datetime.strptime(to_, '%Y%m%d%H%M%S')

        last_known_tara = self.last_known_tara_container(id)
        container_sesions = self.get_item_container_sessions(id, from_, to_)

        if last_known_tara == 'na' and container_sesions == []:
            return []

        return {
            'id': id,
            'tara': last_known_tara,
            'sessions': container_sesions
        }

    def last_known_tara_container(self, id):
        self.db_cursor.execute(
            f"SELECT weight, unit FROM containers_registered WHERE container_id = '{id}'"
        )
        rows = self.db_cursor.fetchall()
        print(rows)
        if not len(rows) > 0:
            return 'na'
        return f'{rows[0][0]} {rows[0][1]}'

    def get_item_container_sessions(self, id, from_, to_):
        self.db_cursor.execute(
            f"SELECT id FROM transactions WHERE (containers LIKE '%{id}%') AND (datetime > '{from_}' AND datetime < '{to_}')"
        )
        rows = self.db_cursor.fetchall()

        return [i[0] for i in rows]

    def session_exists(self, id):
        self.db_cursor.execute(
            f"SELECT id FROM transactions WHERE id = {id}"
        )
        row = self.db_cursor.fetchall()
        if len(row) > 0:
            return True
        return False

    def get_session(self, id):
        self.db_cursor.execute(
            f"SELECT * FROM transactions WHERE id = {id}"
        )
        rows = self.db_cursor.fetchone()
        #print('session', rows)
        results = {}
        results['id'] = id

        truck = rows[3]
        #print('truck', truck)
        if truck == '' or truck == None:
            truck = 'na'
        results['truck'] = truck

        results['bruto'] = rows[5]

        direction = rows[2]
        if direction == 'out':
            results['truckTara'] = rows[6]
            results['neto'] = self.session_neto(rows[4], rows[5], rows[6])

        return results

    def session_neto(self, cont_ids, bruto, truckTara):
        sum_of_conts = 0
        #print('c_ids', cont_ids)
        cont_ids_split = cont_ids.split(',')

        for cont in cont_ids_split:
            #print('c', cont)

            self.db_cursor.execute(
                f"SELECT * FROM containers_registered WHERE container_id = '{cont}'"
            )
            row = self.db_cursor.fetchone()
            print('specific container', row)
            try:
                if row[2] == 'kg':
                    sum_of_conts = sum_of_conts + row[1]
                else:
                    sum_of_conts = sum_of_conts + (row[1]*0.453592)
            except:
                return 'na'

        return bruto - truckTara - sum_of_conts

    def batch_weight_handler(self, df, clm, multiplier):

        # for ind, row in df.iterrows():
        #     print(
        #         f"id: {row[id]} weight: {row[clm['weight']]}")
        batch_result = []
        for i in range(len(df)):
            #print(df.loc[i, "id"], df.loc[i, f"{clm['weight']}"])
            batch_result.append(self.batch_weight_handle_containers(id=df.loc[i, "id"],
                                                                    weight_in_kg=df.loc[i,
                                                                                        f"{clm['weight']}"]*multiplier))
            # else:
            #     batch_error += self.batch_weight_handle_trucks(id=df.loc[i, "id"],
            #                                                    weight_in_kg=df.loc[i, f"{clm['weight']}"]*multiplier)

        # if batch_error == 0:
        #     print(batch_error)
        #     return 'success'
        return batch_result

    def batch_weight_handle_containers(self, id, weight_in_kg, unit='kg'):
        exists = self.does_container_exists(cont_id=id)
        if exists:
            # update db
            self.db_cursor.execute(
                f"UPDATE containers_registered SET weight = {weight_in_kg}, unit = '{unit}' WHERE container_id = '{id}'")
            self.db.commit()

            if self.db_cursor.rowcount == 1:
                print(self.db_cursor.rowcount)
                print('batch container updated')

            else:
                print(self.db_cursor.rowcount)
                print('couldnt commit batch container')

        else:
            # add to db
            self.db_cursor.execute(
                f"INSERT INTO containers_registered(container_id, weight, unit) values('{id}', {weight_in_kg}, '{unit}')")
            self.db.commit()
            if self.db_cursor.rowcount == 1:
                print(self.db_cursor.rowcount)
                print('batch container added')

            else:
                print(self.db_cursor.rowcount)
                print('couldnt commit batch container')

        return {
            'id': id,
            'weight': weight_in_kg,
            'unit': unit
        }

    def batch_weight_handle_trucks(self, id, weight_in_kg):
        return 0
