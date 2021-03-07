from datetime import datetime


# Queries for members resource
class Member:
    @staticmethod
    def insert_member(data):
        sql = """INSERT INTO raxogym.members (name, address, age, gender, email, joining_date, batch, mobile_number, 
        personal_trainer, city, height, weight, blood_group, profile_pic, branch_id, is_active) VALUES('{}', '{}', {},
         '{}', '{}', '{}', '{}', '{}', '{}', '{}', {}, {}, '{}', '{}', (select active_branch_id 
         from admin where adminId = {}), {}); """
        query = sql.format(data.get('name'), data.get('address'), data.get('age'), data.get('gender'),
                           data.get('email'), data.get('joining_date',
                                                       datetime.strftime(datetime.now(), '%Y-%m-%d')),
                           data.get('batch'), data.get('mobile_number'),
                           data.get('trainer'),
                           data.get('city'), data.get('height'), data.get('weight'),
                           data.get('blood_group'), data.get('profile_pic', 'Null'),
                           data.get('admin_id'), True)
        return query

    @staticmethod
    def insert_subscription(data):
        sql_query = """INSERT INTO raxogym.member_subscription (memberId, subscriptionId, subscription_start_date, 
        subscription_end_date, amount_paid, created_on, remaining_payment_date, subscription_is_active, 
        advance_subscription)VALUES((SELECT memberId from members where email='{}'), {}, '{}', '{}', {}, 
        CURRENT_TIMESTAMP, '{}', {}, {}); """
        return sql_query.format(data.get('email'), data.get('subscription_id'),
                                data.get('joining_date'),
                                '2020-05-21', data.get('amount_paid'),
                                data.get('remaining_payment_date', datetime.strftime(datetime.now(), '%Y-%m-%d')),
                                True, False)

    @staticmethod
    def user_by_email(email):
        sql_query = """SELECT memberId, name, address, age, gender, email, subscription_type, 
        DATE_FORMAT(joining_date,'%d %M %Y') AS registered_on, batch, amount_paid, amount_left, mobile_number, 
        personal_trainer, city, height, weight, base_amount, blood_group, profile_pic, subscription_is_active, 
        branch_id, is_active FROM raxogym.members where email = '{}';"""
        return sql_query.format(email)

    @staticmethod
    def get_by_branch_id(admin_id):
        sql_query = """SELECT rm.memberId, name,'gym_member' as `type`,(SELECT true where rms.subscription_is_active or 
        rms.advance_subscription) as subscription_is_active, address, age, gender, email, 
        DATE_FORMAT(joining_date,'%d %M %Y') AS JoininDate, 
        (rs.base_amount - rms.amount_paid ) as amount_left_to_be_paid,batch, 
        mobile_number, 
        personal_trainer, city, height, weight, blood_group, profile_pic, 
        rm.branch_id FROM raxogym.members rm 
        inner join raxogym.member_subscription  rms on
        rms.memberId  = rm.memberId 
        inner join raxogym.subscription rs on 
        rs.subscriptionId = rms.subscriptionId 
        where rm.branch_id = (SELECT active_branch_id from raxogym.admin where adminId={});"""
        return sql_query.format(admin_id)

    @staticmethod
    def subscription(branch_id):
        sql_query = """
         select member_subscriptionId,memberId, DATE_FORMAT(subscription_start_date, '%d %M %Y') as subscriptionStartDate, 
        DATE_FORMAT(subscription_end_date, '%d %M %Y') as subscriptionEndDate,
        amount_paid, DATE_FORMAT(created_on, '%d %M %Y') as subscriptionCreationDate, 
        subscription_is_active, subscription_type,
        base_amount, advance_subscription from raxogym.member_subscription rms
        inner join raxogym.subscription rs on 
        rms.subscriptionId = rs.subscriptionId where branch_id = (SELECT active_branch_id from raxogym.admin 
        where adminId={});
        """
        return sql_query.format(branch_id)

    @staticmethod
    def get_by_user_id(user_id):
        sql_query = """SELECT id, name, address, age, gender, email, subscription_type, joining_date, batch, amount_paid, amount_left, payment_date, mobile_number, personal_trainer, city, height, weight, base_amount, blood_group, profile_pic, subscription_is_active, branch_id
                    FROM raxogym.members where id = {};
                    """
        return sql_query.format(user_id)

    @staticmethod
    def update_member(data):
        sql_query = """UPDATE raxogym.members SET name='{}', address='{}', age={}, gender='{}', email='{}',
        subscription_type='{}', batch='{}', amount_paid={}, amount_left={},
        payment_date='{}', mobile_number={}, personal_trainer='{}', city='{}', height={}, weight={}, base_amount={},
        blood_group='{}', profile_pic={}, subscription_is_active={}, branch_id={} WHERE id={}; """
        query = sql_query.format(data.get('name'), data.get('address'), data.get('age'), data.get('gender'),
                                 data.get('email'), data.get('subscription'),
                                 data.get('batch'), data.get('amount_paid'), data.get('amount_left'),
                                 data.get('payment_date'), data.get('mobile_number'),
                                 data.get('personal_trainer'),
                                 data.get('city'), data.get('height'), data.get('weight'),
                                 data.get('base_amount'),
                                 data.get('blood_group'), data.get('profile_pic'),
                                 data.get('subscription_is_active', True),
                                 data.get('branch_id'),
                                 data.get('id'))
        return query
