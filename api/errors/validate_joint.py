from datetime import datetime, date
from uploads.models import Gljointmst,Glmploan,Schememaster,Membermaster,Glclmast


def validate_columns_joint(data):
    errors = []

    columns = [jon for jon in data]

    columns_joint = [
                     'policy_no','client_no','loan_no','surname','other_names','title','status',
                     'commence_date','birth_date','age','marital_sta','principle_m','loan_amount'
                    ]

    if len(columns) > 0:
        for column_name in columns_joint:
            if columns.count(str(column_name)) == 0:
                errors.append(f"{column_name} is missing in post data")
    else:
        errors.append("No post data has been submitted")

    # mandatory fields
    if len(errors) == 0:
        for val in columns_joint:
            if len(data[val]) == 0 and data[val] == "":
                errors.append(f"{val} is a Mandatory Field ")

    return errors


def validate_joint_member(data):
    errors = []

    errors = validate_columns_joint(data)

    if len(errors) == 0 :

        #  decimal fields
        decimal_fields =  [
            'loan_amount',
        ]

        # check for decimal fields
        for val in decimal_fields:
            if str(data[val]).isdecimal():
                errors.append(f"{val} should be a Decimal field ")
        try:
            datetime.strptime(data['commence_date'], "%d/%m/%Y")
        except ValueError:
            errors.append('Invalid date format on commence_date field [dd/mm/YYYY]')

        try:
            datetime.strptime(data['birth_date'], "%d/%m/%Y")
        except ValueError:
            errors.append('Invalid date format on birth_date field [dd/mm/YYYY]')

        if Schememaster.objects.filter(policy_no=data['policy_no']).count() <= 0:
            errors.append('The policy number does not exist in AIMS')

        if Membermaster.objects.filter(policy_no=data['policy_no'], client_no=(data['client_no']).strip()).count() <= 0:
            errors.append('The client number does not exist in the scheme ')
        if Glclmast.objects.filter(client_no=(data['client_no']).strip()).count() <= 0:
            errors.append('The client number does not exist in AIMS')

        if float(data['loan_amount']) <= 0:
            errors.append("The loan amount should be greater than zero")

        if int(data['age']) <= 0:
            errors.append("The age should be greater than zero")
        if int(data['age']) > 200:
            errors.append("Invalid age ")

    return errors