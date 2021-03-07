import os
from flask import Flask, request
from flask_restful import Resource, Api
from werkzeug.security import check_password_hash
from models.admin import Admin
from resources.admin import (AdminRegister, AdminLogout, TokenRefresh, ResetPassword, GetOrganisation, UpdateProfile)
from resources.organisation import OrganisationResigter, BranchRegister
from resources.member import MemberRegister, GetMember, UpdateMember
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from blacklist import BLACKLIST
from src.response import Response
from flask_jwt_extended import create_access_token, create_refresh_token
from resources.image import UploadImage, GetImage
from src.constants import Constants
from library.flask_uploads.flask_uploads import configure_uploads, patch_request_class
from library.image.images import IMAGES_SET

constants = Constants()
response = Response()

app = Flask(__name__)
CORS(app)
api = Api(app)

app.config["JWT_BLACKLIST_ENABLED"] = True  # enable blacklist feature
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = [
    "access",
    "refresh",
]  # allow blacklisting for access and refresh tokens
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
app.secret_key = "_g!y@m$as#e&crete_"  # could do app.config['JWT_SECRET_KEY'] if we prefer

jwt = JWTManager(app)

app.config['UPLOADED_IMAGES_DEST'] = os.path.join("static", "images")


# This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST


patch_request_class(app, 10 * 1024 * 1024)  # 1o MB max size upload
configure_uploads(app, IMAGES_SET)


class Home(Resource):
    @staticmethod
    def get():
        return response.home()

    @staticmethod
    def post():
        return response.home()


# Using the user_claims_loader, we can specify a method that will be
# called when creating access tokens, and add these claims to the said
# token. This method is passed the identity of who the token is being
# created for, and must return data that is json serializable
@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    query = Admin.get_by_id(identity)
    user_info = constants.receive_query(query)
    user_info = user_info['data'][0]
    return {
        "org_id": user_info['org_id'],
        "branch_id": user_info['active_branch_id'],
        "user": {
            "id": identity,
            "public_id": user_info['public_id'],
            "is_active": user_info['is_active'],
            "email": user_info['email'],
        }
    }


class AdminLogin(Resource):
    @staticmethod
    def post():
        try:
            data = request.get_json()['data']
            email = data['email']
            password = data['password']
            query = Admin.get_by_email(email)
            valid_user = constants.receive_query(query)
            if not valid_user['data']:
                return response.not_found("You don't have user account.")
            valid_user = valid_user['data'][0]
            if check_password_hash(valid_user['password'], password):
                access_token = create_access_token(identity=valid_user['adminId'], fresh=True)
                # access_token = create_access_token(valid_user.id)
                refresh_token = create_refresh_token(valid_user['adminId'])
                return {
                           "status": {
                               "code": 200,
                               "value": "login successfully",
                           },
                           "data": {
                               "username": valid_user['name'],
                               "access_token": access_token,
                               "refresh_token": refresh_token
                           }
                       }, 200
            else:
                return response.invalid_credential("password is not valid")
        except Exception as ex:
            return response.exception(ex)


api.add_resource(Home, '/')
api.add_resource(AdminRegister, '/admin-register')
api.add_resource(MemberRegister, '/member-register')
api.add_resource(AdminLogin, '/login')
api.add_resource(AdminLogout, '/logout')
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(OrganisationResigter, "/organisation-register")
api.add_resource(BranchRegister, "/branch-register")
api.add_resource(GetOrganisation, '/get-organisation')
# api.add_resource(GenerateSecretQuestion, '/generate-secret-question')
api.add_resource(UploadImage, '/upload-image')
api.add_resource(GetImage, '/image/<string:filename>')
api.add_resource(ResetPassword, '/change-password')
api.add_resource(UpdateProfile, '/update-profile')
api.add_resource(GetMember, '/get-all-members')
api.add_resource(UpdateMember, '/update-member')

# TODO pending job to complete
"""
get-organisation 
    # change data_type of avatar
    1. trainer list
    2. check batch true or false
        - if true then show batch list
    3. subscription list
        - base amount 
#API
renew subscription

subscription_is_active: False/True
"""
if __name__ == '__main__':
    app.run()
