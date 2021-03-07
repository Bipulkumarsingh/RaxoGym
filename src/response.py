from src.constants import Constants

constants = Constants()


class Response:
    @staticmethod
    def home():
        constants.STATUS200['status']['code'] = 200
        constants.STATUS200['status']['value'] = 'OK'
        constants.STATUS200['data'] = 'Success'
        return constants.STATUS200

    @staticmethod
    def exception(message):
        constants.STATUS200['status']['code'] = 500
        constants.STATUS200['status']['value'] = 'Internal server error'
        constants.STATUS200['data'] = message
        return constants.STATUS200

    @staticmethod
    def created(message):
        constants.STATUS200['status']['code'] = 201
        constants.STATUS200['status']['value'] = 'Created'
        constants.STATUS200['data'] = message
        return constants.STATUS200

    @staticmethod
    def not_found(message):
        constants.STATUS200['status']['code'] = 404
        constants.STATUS200['status']['value'] = 'Not Found'
        constants.STATUS200['data'] = message
        return constants.STATUS200

    @staticmethod
    def conflict(message):
        constants.STATUS200['status']['code'] = 409
        constants.STATUS200['status']['value'] = 'Not Found'
        constants.STATUS200['data'] = message
        return constants.STATUS200

    @staticmethod
    def profile_updated(message):
        constants.STATUS200['status']['code'] = 202
        constants.STATUS200['status']['value'] = 'updated'
        constants.STATUS200['data'] = message
        return constants.STATUS200

    @staticmethod
    def profile_pic_update(message):
        constants.STATUS200['status']['code'] = 202
        constants.STATUS200['status']['value'] = 'Pic updated'
        constants.STATUS200['data'] = message
        return constants.STATUS200

    @staticmethod
    def invalid_credential(message):
        constants.STATUS200['status']['code'] = 406
        constants.STATUS200['status']['value'] = 'Not Accepted'
        constants.STATUS200['data'] = message
        return constants.STATUS200

    @staticmethod
    def get_info(message):
        constants.STATUS200['status']['code'] = 200
        constants.STATUS200['status']['value'] = 'OK'
        constants.STATUS200['data'] = message
        return constants.STATUS200
