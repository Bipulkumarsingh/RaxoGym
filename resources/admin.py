from flask_restful import Resource, reqparse
from flask import request
from models.admin import Admin, Branch, Organisation, Trainer, Batch, Subscription
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from blacklist import BLACKLIST
from src.response import Response
from src.constants import Constants
from flask_jwt_extended import (
    create_access_token,
    get_jwt_claims,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
)

constants = Constants()
response = Response()


# def str_bool(s):
#     if s.lower() == "true":
#         return True
#     else:
#         return False


class AdminRegister(Resource):
    @staticmethod
    def post():
        try:
            data = request.get_json()['data']
            query = Branch.check_branch(data.get('active_branch_id'), data.get('org_id'))
            branch = constants.receive_query(query)
            super_admin = data.get('super_admin', 'False')
            profile_pic = data.get('profilePic', None)
            if branch['data']:
                query = Admin.get_by_email(data.get('email'))
                past_admin = constants.receive_query(query)
                if past_admin['data']:
                    return response.conflict("A user with this email already exists")
                else:
                    hash_password = generate_password_hash(data['password'], method='sha256')
                    query = Admin.insert_admin(data['name'], hash_password, data['email'], profile_pic, str(uuid.uuid4()),
                                               data['active_branch_id'], data['org_id'],
                                               super_admin, data['mobile_number'], True)

                    value = constants.insert_query(query)
                    return value
            else:
                query = Organisation.get_by_id(data.get('org_id'))
                if not constants.receive_query(query)['data']:
                    return response.not_found("Organisation not found")
                else:
                    return response.not_found("Branch not found.")
        except Exception as ex:
            return response.exception(ex)


# class AdminLogin(Resource):
#     parser = reqparse.RequestParser()
#     parser.add_argument('email',
#                         type=str,
#                         required=True,
#                         help="This field cannot be blank."
#                         )
#     parser.add_argument('password',
#                         type=str,
#                         required=True,
#                         help="This field cannot be blank."
#                         )
#
#     def post(self):
#         try:
#             data = AdminLogin.parser.parse_args()
#             email = data['email']
#             password = data['password']
#             valid_user = AdminModel.find_by_email(email)
#             if valid_user is None:
#                 return not_found("You don't have user account.")
#             if check_password_hash(valid_user.password, password):
#                 access_token = create_access_token(identity=valid_user.id, fresh=True)
#                 # access_token = create_access_token(valid_user.id)
#                 refresh_token = create_refresh_token(valid_user.id)
#                 return {
#                            "status": {
#                                "code": 200,
#                                "value": "login successfully",
#                            },
#                            "data": {
#                                "username": valid_user.username,
#                                "access_token": access_token,
#                                "refresh_token": refresh_token
#                            }
#                        }, 200
#             else:
#                 return {
#                            "status": {
#                                "code": 400,
#                                "value": "Invalid credentials"
#                            },
#                            "data": {
#                                "username": valid_user.username
#                            }
#                        }, 200
#         except Exception as e:
#             return exception()


class AdminLogout(Resource):
    @jwt_required
    def token_check(self):
        jti = get_raw_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT.
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return user_id

    def post(self):
        try:
            user_id = self.token_check()
            # return {"message": "User <id={}> successfully logged out.".format(user_id)}, 200
            return {
                       "status": {
                           "code": 200,
                           "value": "logout success"
                       },
                       "data": {
                           "message": "User id: {} successfully logged out.".format(user_id)
                       }
                   }, 200
        except Exception as e:
            return response.exception(e)


class ResetPassword(Resource):
    @staticmethod
    @jwt_required
    def post():
        data = request.get_json()['data']
        try:
            user = get_jwt_identity()
            query = Admin.get_by_id(user)
            valid_user = constants.receive_query(query)['data'][0]
            if check_password_hash(valid_user.get('password'), data['currentPassword']):
                hash_password = generate_password_hash(data['newPassword'], method='sha256')
                query = Admin.update_password(hash_password, valid_user['adminId'])
                password_change = constants.update_query(query)
                return password_change
            else:
                return response.invalid_credential("password is not valid.")
        except Exception as ex:
            return response.exception(ex)


class UpdateProfile(Resource):
    @staticmethod
    @jwt_required
    def post():
        data = request.get_json()['data']
        user_id = get_jwt_identity()
        try:
            query = Admin.get_by_id(user_id)
            user = constants.receive_query(query)['data'][0]
            name = data.get('name', user['name'])
            mobile_number = data.get('mobile_number', user['mobile_number'])
            avatar = data.get('profilePic', user['profilePic'])
            query = Admin.update_admin(user_id, name, mobile_number, avatar)
            profile_update = constants.update_query(query)
            return profile_update
        except Exception as ex:
            return response.exception(ex)


class GetOrganisation(Resource):
    @jwt_required
    def post(self):
        data = request.get_json()['data']
        user_id = get_jwt_identity()
        query = Admin.get_by_id(user_id)
        user = constants.receive_query(query)['data'][0]
        claims = get_jwt_claims()
        active_branch_id = data.get('active_branch_id', user['active_branch_id'])
        if user:
            if user['super_admin']:
                query = Branch.get_by_org(claims['org_id'])
                branch_list = constants.receive_query(query)['data']
            else:
                branch_list = []
            if data.get('active_branch_id', None):
                query = Admin.update_active_branch(data.get('active_branch_id'), user.get('adminId'))
                constants.update_query(query)
            trainer_query = Trainer.get_by_branch(active_branch_id)
            trainer = constants.receive_query(trainer_query)['data']
            batch_query = Batch.get_by_branch(active_branch_id)
            batch = constants.receive_query(batch_query)['data']
            subscription_query = Subscription.get_by_branch(active_branch_id)
            subscription_type = constants.receive_query(subscription_query)['data']
            query = Branch.get_by_id(active_branch_id)
            branch_info = constants.receive_query(query)['data'][0]
            active_branch = {
                "branch_id": active_branch_id,
                "branch_name": branch_info['branch_name'],
                "incharge": branch_info['incharge'],
                "address": branch_info['address'],
                "is_active": branch_info['is_active']
            }
            claims['active_branch'] = active_branch
            claims['branches'] = branch_list
            profile_pic = user['profilePic']
            claims['user']['name'] = user['name']
            claims['user']['mobile_number'] = user['mobile_number']
            claims['user']['profilePic'] = profile_pic
            claims['user']['super_admin'] = user['super_admin']
            claims['trainerList'] = trainer
            claims['batchList'] = batch
            claims['subscriptionList'] = subscription_type
            return response.get_info(claims)
        return response.not_found("User Not Found")


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200


# class Trainer(Resource):
#     parser = reqparse.RequestParser()
#     parser.add_argument('name',
#                         type=str,
#                         required=True,
#                         help="please provide trainer name"
#                         )
#
#     def post(self):
#         data = self.parser.parse_args()
