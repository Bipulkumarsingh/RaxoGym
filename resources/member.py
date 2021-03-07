from flask_restful import Resource
from flask import request
from datetime import datetime
from models.member import Member
from src.constants import Constants
from flask_jwt_extended import (jwt_required, get_jwt_claims)
from src.response import Response

constants = Constants()
response = Response()


class MemberRegister(Resource):
    @staticmethod
    @jwt_required
    def post():
        # TODO if we have multiple organisation with same org name
        try:
            data = request.get_json()['data']
            previous_user = constants.receive_query(Member.user_by_email(data['email']))
            if previous_user['data']:
                return response.conflict("User with this email already exits.")
            # data['joining_date'] = datetime.strptime(data['joining_date'], '%Y-%m-%d')
            # data['joining_date'] = datetime.timestamp(joining_date)
            claims = get_jwt_claims()
            data['admin_id'] = claims['user']['id']
            query = Member.insert_member(data)
            user_created = constants.insert_query(query)
            if not user_created['data']:
                return user_created
            subscription_query = Member.insert_subscription(data)
            subscription = constants.insert_query(subscription_query)
            return subscription
        except Exception as ex:
            return response.exception(ex)


class GetMember(Resource):
    @staticmethod
    @jwt_required
    def get():
        claims = get_jwt_claims()
        query = Member.get_by_branch_id(claims['user']['id'])
        members = constants.receive_query(query)
        subscription_query = Member.subscription(claims['user']['id'])
        subscription = constants.receive_query(subscription_query)
        members['data'].append({"subscription": subscription['data']})
        return members


class UpdateMember(Resource):
    @jwt_required
    def put(self):
        claims = get_jwt_claims()
        try:
            data = request.get_json()
            data['branch_id'] = claims.get('branch_id')
            data['id'] = 4
            data['joining_date'] = datetime.strptime(data['joining_date'], '%d/%m/%Y')
            data['payment_date'] = data['joining_date']
            query = Member.update_member(data)
            updated = constants.update_query(query)
            return response.profile_updated(updated)
        except Exception as ex:
            return response.exception(ex)
