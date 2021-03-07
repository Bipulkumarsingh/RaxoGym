from library.db.db_connection import Database
# import json


class ConstantsMeta(type):
    _instance = None

    def __call__(self):
        if self._instance is None:
            self._instance = super().__call__()
        return self._instance


class Constants(metaclass=ConstantsMeta):

    def __init__(self):
        self.STATUS200 = {'version': {'version': "1.0.0.0", "name": "Raxoweb"},
                          "status": {"code": None, "value": None},
                          "data": None, 'error': False}
        self.HEADERS = {'content-type': "application/json", 'cache-control': "no-cache"}

    def receive_query(self, query):
        try:
            vp = Database(self.get_config())
            return vp.receive_query(query=query)
        except Exception as e:
            print(e)

    def insert_query(self, query):
        try:
            vp = Database(self.get_config())
            return vp.insert_query(query)
        except Exception as e:
            print(e)

    def execute_query(self, query):
        try:
            vp = Database(self.get_config())
            return vp.execute_query(query=query)["data"]
        except Exception as e:
            print(e)

    def update_query(self, query):
        try:
            vp = Database(self.get_config())
            return vp.update_query(query=query)
        except Exception as e:
            print(e)

    @staticmethod
    # def get_config(org='mysql', json_filename="./configuration/configuration.json"):
    def get_config():
        configuration = {
            "driver": "mysql",
            "host": "127.0.0.1",
            "database": "raxogym",
            "user": "root",
            "password": "R1a2x3o4@777"
        }
        return configuration
        # with open(json_filename, "r") as file:
        #     try:
        #         value = json.load(file)
        #         return value[org]
        #     except KeyError:
        #         return None
