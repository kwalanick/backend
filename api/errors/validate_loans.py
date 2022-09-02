from datetime import datetime, date

from uploads.models import Glmploan,Glclmast,Schememaster,Membermaster


def validate_columns_loans(data):
    errors = []
    columns = [lon for lon in data]


    loan_columns = ['policy_no', 'client_no', 'member_no', 'uw_year', 'commence_date', 'joint_loan', 'loan_amount', 'mod_factor',
                    'interest_basis', 'age', 'term_months', 'term_years', 'interest_rate',
                    'annual_prem_rate', 'premium', 'prorated_prem', 'total_premium', 'admin_charge','rider_premium','rider_benefit','comm_premium'
                    ]


    # check for missing fields in post
    for column_name in loan_columns:
        if columns.count(str(column_name)) == 0:
            errors.append(f"{column_name} is missing in post data")


    # check for mandatory fields
    mandatory_fields = ['policy_no', 'member_no','client_no', 'comm_premium', 'rider_premium', 'rider_benefit', 'uw_year',
                        'commence_date', 'total_premium', 'admin_charge', 'loan_amount', 'annual_prem_rate',
                        'premium',
                        'interest_basis', 'age', 'term_months', 'term_years'
                       ]

    for val in mandatory_fields:
        if len(data[val]) == 0 and data[val] == "":
            errors.append(f"{val} is a Mandatory Field ")

    return errors


def validate_loan_errors(data):
    errors = []
    errors = validate_columns_loans(data)
    if len(errors) == 0:

        #  decimal fields
        decimal_fields = [
            'total_premium', 'admin_charge', 'loan_amount', 'annual_prem_rate', 'premium',
            'interest_rate'
        ]
        # check for decimal fields
        for val in decimal_fields:
            if  str(data[val]).isdecimal() :
                errors.append(f"{val} should be a Decimal field ")
        try:
            datetime.strptime(data['commence_date'], "%d/%m/%Y")
        except ValueError:
            errors.append('Invalid date format on commence_date field [dd/mm/YYYY]')
        if Schememaster.objects.filter(policy_no=data['policy_no']).count() <= 0:
            errors.append('The policy number does not exist in AIMS')
        if Membermaster.objects.filter(policy_no=data['policy_no'], member_no=(data['member_no']).strip()).count() <= 0:
            errors.append('The member does not exist in the scheme ')
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

        if data['interest_basis'] not in ['F','B'] or len(data['interest_basis']) != 1:
            errors.append('The interest_basis should either be (B) - Reducing Balance or (F) - Fixed ')

        if data['premium'] is None or data['premium'] == 0:
            errors.append('The premium should not be null or 0')

        if data['total_premium'] is None or data['total_premium'] == 0:
            errors.append('The total premium should not be null or 0')

        if data['prorated_prem'] is None or data['prorated_prem'] == 0:
            errors.append('The total premium should not be null or 0')

        if data['term_months'] is None or data['term_months'] == 0:
            errors.append('The term months should not be null or 0')

        if data['term_years'] is None or data['term_years'] == 0:
            errors.append('The term years should not be null or 0')

        return errors

    return errors





