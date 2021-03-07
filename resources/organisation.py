from flask_restful import Resource
from flask import request
from models.admin import Branch, Organisation
from src.response import Response
from src.constants import Constants

constants = Constants()
response = Response()


class OrganisationResigter(Resource):
    @staticmethod
    def post():
        try:
            data = request.get_json()['data']
            org_name = data['name'].lower()
            org_owner = data.get('owner')
            address = data['address']
            branch_name = data['branch_name'].lower()
            incharge = data['incharge']
            past_org = constants.receive_query(Organisation.get_by_name(org_name))
            if past_org['data']:
                org_id = past_org['data'][0]['orgId']
            else:
                query = Organisation.insert_org(org_name, org_owner)
                constants.insert_query(query)
                org = constants.receive_query(Organisation.get_by_name(org_name))
                org_id = org['data'][0]['orgId']
            query = Branch.get_by_name(branch_name, org_id)
            past_branch = constants.receive_query(query)
            if past_branch['data'] and [1 for org in past_branch['data'] if org.get('org_id') == org_id]:
                return response.conflict('Branch with this branch name already exists in this organisation.')
            branch = Branch.insert_branch(branch_name, address, incharge, org_id, True)
            inserted = constants.insert_query(branch)
            return inserted
        except Exception as ex:
            return response.exception(ex)


class BranchRegister(Resource):
    @staticmethod
    def post():
        try:
            data = request.get_json()['data']
            org_id = data.get('org_id')
            branch_name = data.get('branch_name').lower()
            address = data.get('address')
            incharge = data.get('incharge')
            org_query = Organisation.get_by_id(org_id)
            past_org = constants.receive_query(org_query)
            branch_query = Branch.get_by_name(branch_name, org_id)
            past_branch = constants.receive_query(branch_query)
            if past_org['data']:
                if past_branch['data']:
                    return response.conflict("Branch with this branch name already exists in this organisation.")
                branch = Branch.insert_branch(branch_name, address, incharge, org_id, True)
                branch_created = constants.insert_query(branch)
                return branch_created
            else:
                return response.not_found("Organisation Not Found.")
        except Exception as ex:
            return response.exception(ex)
