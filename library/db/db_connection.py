from psycopg2 import connect as postgres_connect, extras
from mysql import connector
from mysql.connector import FieldType


class Database:
    """ This is some connection """

    def __init__(self, config=None):
        self.cursor_type = None
        self.db = None
        self.config = self.get_config(config)
        self.connection = self.create_connection()

    def get_config(self, config):
        if isinstance(config, dict):
            self.db = config.get("driver")
            config.pop("driver")
            return config

    def create_connection(self):
        if "postges" in self.db:
            return postgres_connect(**self.config)
        elif "mysql" in self.db:
            return connector.connect(**self.config)

    def create_cursor(self, cursor_type="list"):
        self.cursor_type = cursor_type
        if "postges" in self.db:
            return self.connection.cursor(self.cursor_type)
        elif "mysql" in self.db:
            if cursor_type == 'list':
                return self.connection.cursor()
            else:
                return self.connection.cursor(dictionary=True)

    def set_data(self, query):
        try:
            cursor = self.create_cursor()
            cursor.execute(query)
            # affected_rows = cursor.rowcount
            # try:
            #     last_inserted_id = cursor.lastrowid
            # except Exception as ex:
            #     cursor.fetchall()
            #     last_inserted_id = cursor.rowcount

            self.connection.commit()
            cursor.close()
            self.connection.close()
            return {'data': 1,
                    'error': False,
                    'status': {'code': '200', 'value': 'Success'},
                    'version': {'name': 'Raxoweb', 'version': '1.0.0.0'}}

        except Exception as ex:
            return {'data': 0,
                    'sqlError': str(ex),
                    'error': False,
                    'status': {'code': '200', 'value': 'Success'},
                    'version': {'name': 'Raxoweb', 'version': '1.0.0.0'}}

    def execute_query(self, query, cursor_type='list'):
        # self.cursor_type = cursor_type

        try:
            cursor = self.create_cursor(cursor_type)
            cursor.execute(query)
            query_result = cursor.fetchall()

            total_rows = cursor.rowcount
            meta_data = []

            for col_index, desc in enumerate(cursor.description):
                if "mysql" in self.db:
                    meta_data.append({'colIndex': col_index,
                                      'colName': desc[0],
                                      'colType': FieldType.get_info(desc[1])})

                elif "postgres" in self.db:
                    meta_data.append({'colIndex': col_index,
                                      'colName': desc.name,
                                      'colType': desc.data_types()[desc.type_code].capitalize()})

            cursor.close()
            self.connection.close()
            resp = {'data': {'result': {'metaData': meta_data,
                                        'queryInfo': {'totalRows': total_rows, 'type': 'selected'},
                                        'resultSet': query_result}},
                    'error': False,
                    'status': {'code': '200', 'value': 'Success'},
                    'version': {'name': 'Raxoweb', 'version': '1.0.0.0'}}

            return resp

        except Exception as ex:

            return {'data': None,
                    'error': False,
                    'sqlError': str(ex),
                    'status': {'code': '200', 'value': 'Success'},
                    'version': {'name': 'Raxoweb', 'version': '1.0.0.0'}}

    def receive_query(self, query, cursor_type='dict'):
        # self.cursor_type = cursor_type
        try:

            cursor = self.create_cursor(cursor_type)
            cursor.execute(query)
            query_result = cursor.fetchall()

            cursor.close()
            self.connection.close()
            resp = {'data': query_result,
                    'error': False,
                    'status': {'code': '200', 'value': 'Success'},
                    'version': {'name': 'Raxoweb', 'version': '1.0.0.0'}}
            return resp

        except Exception as ex:

            return {'data': None,
                    'error': False,
                    'sqlError': str(ex),
                    'status': {'code': '200', 'value': 'Success'},
                    'version': {'name': 'Raxoweb', 'version': '1.0.0.0'}}

    def insert_query(self, query):
        return self.set_data(query)

    def update_query(self, query):
        return self.set_data(query)

    def delete(self, query):
        return self.set_data(query)


if __name__ == "__main__":
    pass
