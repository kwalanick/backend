from datetime import datetime, date
from uploads.models import Glmmridtl,Schememaster,Membermaster,Glclmast


def validate_rider_columns(data):
    errors = []

    columns = [rid for rid in data]

    rider_columns = ['policy_no','uw_year','client_no','member_no','rider_code','benefit','rate','premium',
                     'retrenchment','retrenchment_period','loan_no']

    if len(columns) > 0:
        # missing columns
        for column_name in rider_columns:
            if columns.count(str(column_name)) == 0:
                errors.append(f"{column_name} is missing in post data")
        
    else:
        errors.append("No post data has been submitted")




    return errors


def validate_riders(data):

    errors = []

    errors = validate_rider_columns(data)

    if len(errors) == 0:

        if Schememaster.objects.filter(policy_no=data['policy_no']).count() <= 0:
            errors.append('The policy number does not exist in AIMS')
        if Membermaster.objects.filter(policy_no=data['policy_no'], member_no=(data['member_no']).strip()).count() <= 0:
            errors.append('The member does not exist in the scheme ')
        if Membermaster.objects.filter(policy_no=data['policy_no'], client_no=(data['client_no']).strip()).count() <= 0:
            errors.append('The client number does not exist in the scheme ')
        if Glclmast.objects.filter(client_no=(data['client_no']).strip()).count() <= 0:
            errors.append('The client number does not exist in AIMS')



    return errors
