from datetime import datetime, date
from uploads.models import Schememaster,Membermaster,Glclmast,Glmploan



def validate_health_columns(data):
    errors = []
    columns = [hq for hq in data]

    health_columns = ['policy_no','uw_year','member_no','client_no','loan_no','q1',
                       'q1description','q2','q2description','weight','height']

    for column_name in health_columns:
        if columns.count(str(column_name)) == 0:
            errors.append(f"{column_name} is missing in post data")

    # mandatory fields
    if len(errors) == 0:
        for val in health_columns:
            if len(data[val]) == 0 and data[val] == "":
                errors.append(f"{val} is a Mandatory Field ")

    return errors


def validate_health_records(data):
    errors = []

    errors = validate_health_columns(data)

    if len(errors) == 0:

        if Schememaster.objects.filter(policy_no=data['policy_no']).count() <= 0:
            errors.append('The policy number does not exist in AIMS')
        if Membermaster.objects.filter(policy_no=data['policy_no'], member_no=(data['member_no']).strip()).count() <= 0:
            errors.append('The member does not exist in the scheme ')
        if Membermaster.objects.filter(policy_no=data['policy_no'], client_no=(data['client_no']).strip()).count() <= 0:
            errors.append('The client number does not exist in the scheme ')
        if Glclmast.objects.filter(client_no=(data['client_no']).strip()).count() <= 0:
            errors.append('The client number does not exist in AIMS')
        if Membermaster.objects.filter(policy_no=data['policy_no'], member_no=(data['member_no']).strip()).count() <= 0:
            errors.append('The member does not exist in the scheme ')
        if Glmploan.objects.filter(policy_no=data['policy_no'], member_no=data['member_no'], loan_no=data['loan_no']
                                   ).count() <= 0:
            errors.append('The loan no specified does not exist in AIMS')
            
        if len(data['uw_year']) > 4 :
            errors.append('The uw_year should not be greater than 4 digits')

        if len(data['weight']) > 5 :
            errors.append('weight should have a maximum of 5 char .')

        if len(data['height']) > 5 :
            errors.append('height should have a maximum of 5 char .')


    return errors
