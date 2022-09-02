import re
from datetime import datetime, date
from uploads.models import Glclmast,Schememaster,Membermaster

def validate_columns_member(data):

    errors = []

    columns = [mem for mem in data]

    member_columns = ['status_code', 'policy_no', 'member_no', 'client_no', 'institute_client_number', 'payroll_no', 'join_date', 'maturity_date', 'employment_date', 'uw_date', 'created_date', 'dob', 'modified_date', 'modified_by',
                       'period_from', 'period_to', 'term_years', 'surname', 'first_name', 'other_names', 'name', 'gender', 'pay_freq', 'monthly_salary', 'annual_salary', 'branch', 'agent', 'retirement_age', 'lc_cover_factor', 'total_sum_assured',
                       'est_loan_amount', 'rider_benefit', 'rider_premium', 'premium', 'age', 'uw_year', 'medical_req', 'annual_prem_rate', 'total_premium', 'account_year', 'account_month', 'comm_amount', 'comm_rate',
                       'received_premium', 'balance', 'loans_granted', 'premium_due_date', 'premium_review_date', 'acquisition_cost', 'non_insurance_prem', 'type_of_bus', 'co_insure', 'company_share', 'dept_no', 'retrenchment', 'retrench_period',
                       'marital_status', 'medical_uw_loading', 'uw_decision']

    for column_name in member_columns:
        if columns.count(str(column_name)) == 0:
            errors.append(f"{column_name} is missing in post data")

    return errors


def validate_member(request, data):
    errors = []
    member_count = 0
    errors = validate_columns_member(data)

    invalidJoinDate = True

    if len(errors) == 0:
        member_count = Membermaster.objects.filter(policy_no=data['policy_no'], client_no=data['client_no']).count()
        print(f"Check policy no from -{data['policy_no']} - {data['client_no']} - {member_count}")

        if Schememaster.objects.filter(policy_no=data['policy_no']).count() <= 0:
            errors.append('The policy no does not exist in AIMS')
        if Glclmast.objects.filter(client_no=data['client_no']).count() <= 0:
            errors.append('Client no specified does not exist in AIMS')
        #if Membermaster.objects.filter(policy_no=data['policy_no'],
           #                            client_no=data['client_no']).count() > 0 and request.method == 'POST':
            #errors.append('The customer already exists in the Scheme')

        try:
            datetime.strptime(data['join_date'], "%d/%m/%Y")
        except ValueError:
            invalidJoinDate = False
            errors.append('Invalid date format on join date field')

        try:
            datetime.strptime(data['employment_date'], "%d/%m/%Y")
        except ValueError:
            errors.append('Invalid date format on employment date field [dd/mm/YYYY]')
        try:
            datetime.strptime(data['uw_date'], "%d/%m/%Y")
        except ValueError:
            errors.append('Invalid date format on uw_date field [dd/mm/YYYY]')
        try:
            datetime.strptime(data['created_date'], "%d/%m/%Y")
        except ValueError:
            errors.append('Invalid date format on creation date field [dd/mm/YYYY]')
        try:
            datetime.strptime(data['dob'], "%d/%m/%Y")
        except ValueError:
            errors.append('Invalid date format on date of birth [dd/mm/YYYY]')
        try:
            datetime.strptime(data['modified_date'], "%d/%m/%Y")
        except ValueError:
            errors.append('Invalid date format on modified_date field [dd/mm/YYYY]')
        try:
            datetime.strptime(data['period_from'], "%d/%m/%Y")
        except ValueError:
            errors.append('Invalid date format on period from field [dd/mm/YYYY]')
        try:
            datetime.strptime(data['period_to'], "%d/%m/%Y")
        except ValueError:
            errors.append('Invalid date format on period to field [dd/mm/YYYY]')

        try:
            datetime.strptime(data['maturity_date'], "%d/%m/%Y")
        except ValueError:
            errors.append('Invalid date format on maturity_date field [dd/mm/YYYY]')


    return errors

