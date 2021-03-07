class Organisation:
    @staticmethod
    def insert_org(name, owner):
        sql_query = """INSERT INTO raxogym.organisation (name, owner, created_on, is_active) VALUES('{}', '{}', 
        CURRENT_TIMESTAMP, 1);"""
        return sql_query.format(name, owner)

    @staticmethod
    def get_by_name(name):
        sql_query = """SELECT orgId, name, owner FROM raxogym.organisation where name = '{}';"""
        return sql_query.format(name)

    @staticmethod
    def get_by_id(org_id):
        sql_query = """SELECT orgId, name, owner FROM raxogym.organisation where orgId = '{}';"""
        return sql_query.format(org_id)


class Branch:
    @staticmethod
    def get_by_name(name, org_id):
        sql_query = """SELECT branchId, address, is_active, incharge, branch_name, org_id, DATE_FORMAT(created_on, '%d %M %Y') AS registered_on FROM raxogym.branch where branch_name = 
        '{}' and org_id= {}; """
        return sql_query.format(name, org_id)

    @staticmethod
    def get_by_org(org_id):
        sql_query = """SELECT branchId, address, is_active, incharge, branch_name, org_id, DATE_FORMAT(created_on, '%d %M %Y') AS registered_on FROM raxogym.branch where org_id = 
        '{}'; """
        return sql_query.format(org_id)

    @staticmethod
    def get_by_id(branch_id):
        sql_query = """SELECT branchId, address, is_active, incharge, branch_name, org_id, DATE_FORMAT(created_on, '%d %M %Y') AS registered_on FROM raxogym.branch where branchId = 
        '{}'; """
        return sql_query.format(branch_id)

    @staticmethod
    def insert_branch(branch_name, address, incharge, org_id, active):
        insert_query = "INSERT INTO raxogym.branch (branch_name, address, incharge, created_on, org_id, is_active) " \
                       "VALUES('{}', '{}', '{}', CURRENT_TIMESTAMP, {}, {});"
        return insert_query.format(branch_name, address, incharge, org_id, active)

    @staticmethod
    def check_branch(branch_id, org_id):
        sql_query = "select branch_name from raxogym.branch where org_id = {} and branchId = {};"
        return sql_query.format(org_id, branch_id)


class Admin:
    @staticmethod
    def get_by_email(email):
        sql_query = """SELECT adminId, public_id, profilePic, name, password, email, is_active, super_admin, mobile_number, 
        org_id, active_branch_id, DATE_FORMAT(created_on, '%d %M %Y') AS registered_on FROM raxogym.admin where email='{}';"""
        return sql_query.format(email)

    @staticmethod
    def get_by_id(user_id):
        sql_query = """SELECT adminId, public_id, profilePic, name, password, email, is_active, super_admin, mobile_number, 
                org_id, active_branch_id, DATE_FORMAT(created_on, '%d %M %Y') AS registered_on FROM raxogym.admin where adminId={};"""
        return sql_query.format(user_id)

    @staticmethod
    def insert_admin(name, password, email, profile_pic, public_id, active_branch, org_id, super_admin, mobile, active):
        sql_query = """INSERT INTO raxogym.admin (public_id, name, email, password, mobile_number, profilePic, 
        created_on, is_active, super_admin, org_id, active_branch_id) VALUES('{}', '{}', '{}', '{}', '{}', '{}', 
        CURRENT_TIMESTAMP, {}, {}, {}, {});"""
        return sql_query.format(public_id, name, email, password, mobile, profile_pic, active, super_admin, org_id,
                                active_branch)

    @staticmethod
    def update_password(password, user_id):
        sql = "UPDATE raxogym.admin SET password='{}' WHERE adminId={};"
        return sql.format(password, user_id)

    @staticmethod
    def update_admin(user_id, name, mobile, profile_pic):
        update_data = """UPDATE raxogym.admin SET name='{}', mobile_number={}, profilePic='{}' where adminId={};"""
        return update_data.format(name, mobile, profile_pic, user_id)

    @staticmethod
    def update_profile_pic(admin_id, profile_pic_id):
        return f"UPDATE raxogym.admin SET profilePic= '{profile_pic_id}' where adminId={admin_id};"

    @staticmethod
    def update_active_branch(branch_id, user_id):
        branch_query = """UPDATE raxogym.admin SET  active_branch_id={} WHERE adminId={};"""
        return branch_query.format(branch_id, user_id)


class Trainer:
    @staticmethod
    def get_by_branch(branch_id):
        return "SELECT trainerId, name, branch_id, DATE_FORMAT(created_on, '%d %M %Y') AS registered_on, is_active FROM " \
               "raxogym.trainer where branch_id = {};".format(branch_id)


class Batch:
    @staticmethod
    def get_by_branch(branch_id):
        return "SELECT batchId, batchType, branch_id, is_active FROM raxogym.batch where branch_id = {};". \
            format(branch_id)


class Subscription:
    @staticmethod
    def get_by_branch(branch_id):
        return "SELECT subscriptionId, subscription_type, base_amount, is_active, branch_id FROM " \
               "raxogym.subscription where branch_id ={};".format(branch_id)
