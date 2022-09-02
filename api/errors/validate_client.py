import re
from datetime import datetime, date

from clients.models import Provinces, Districts, Sectors, Cells, Village, Countryparam, Glidentity, \
    Bnrclassification, Glmasta, NaicsCodes, Glrelation, Glstatus, EconomicSubSectors, Occupation, Gltitle


def validate_columns_client(data):
    errors = []
    columns = [ col for col in data]

    client_columns = ['bnr_classification', 'surname', 'other_names', 'resident_country', 'country_code', 'identity_card_no', 'id_doc', 'gender', 'marital_status', 'spourse_name', 'birth_date', 'birth_reg_village', 'residence_type'
       ,'email', 'mobile_no', 'telephone', 'fax', 'occupation', 'naics_code', 'economic_sub_sector', 'relation_to_company_code', 'province', 'district', 'sector', 'cellule', 'village', 'contact', 'contact_position',
        'contact_telephone', 'title', 'address', 'address2', 'address3']

    for column_name in client_columns:
        if columns.count(str(column_name)) == 0:
            errors.append(f"{column_name} is missing from post data")

    return errors

def validate_client_req(data):
    errors = []
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    # checking missing fields in post data
    errors = validate_columns_client(data)

    print(len(errors))

    if len(errors) == 0:
        # validate bnr classification
        bnr_code = str(data['bnr_classification']).strip()

        if Bnrclassification.objects.filter(bnr_code__contains=int(bnr_code)).count() <= 0:
            errors.append('Invalid bnr classification code .')
        if Glmasta.objects.filter(code=data['marital_status']).count() <= 0:
            errors.append(f'Invalid marital status .')
        if Glidentity.objects.filter(identity_type__contains=data['id_doc']).count() <= 0:
            errors.append(f"Invalid identity type ")
        if NaicsCodes.objects.filter(naics_code=data['naics_code']).count() <= 0:
            errors.append(f"Invalid industry code")
        if EconomicSubSectors.objects.filter(isic_code=data['economic_sub_sector']).count() <= 0:
            errors.append(f"Invalid economic sub sectors ")
        if Glrelation.objects.filter(code__contains=data['relation_to_company_code']).count() <= 0:
            errors.append(f"Invalid relations code")
        try:
            datetime.strptime(data['birth_date'], "%d/%m/%Y")
        except ValueError:
            invalidJoinDate = False
            errors.append('Invalid date format on birth date field - format[dd/mm/YYYY]')

        # id number validations
        if len(data['identity_card_no']) != 16 and data['bnr_classification'] == '001' and data[
            'country_code'] == 'C081':
            errors.append('Please capture ID number in the correct format')
        if str(data['identity_card_no'][5]) not in ['7', '8'] and int(data['id_doc']) == 2:
            errors.append('Error in ID number gender section')
        if len(data['id_doc']) == 0:
            errors.append('Identity type should not be null')

        # validate email
        if not re.fullmatch(regex, data['email']):
            errors.append('Please capture a valid email address at ')

        # validate names
        if not re.match("^[A-Za-z']+$", data['surname']):
            errors.append('Surname should only contain alphabetic characters ')
        # if not re.match("^[A-Za-z']+$", data['other_names']):
        #     errors.append('Other Names should only contain alphabetic characters ')

        if Occupation.objects.filter(occup_code__contains=data['occupation']).count() <= 0:
            errors.append('Invalid occupation code .')

        if len(data['residence_type']) > 1 or data['residence_type'] not in ['T','O']:
            errors.append('Resident type should either be T[Tenant] or O [Owner]')
            
        if len(data['gender']) > 1 or data['gender'] not in ['M', 'F']:
            errors.append('Gender type should either be M[Male] or F [Female]')

        # validate place of birth village
        if Village.objects.filter(village_code=data['birth_reg_village']).count() <= 0:
            errors.append('Incorrect place of birth village code .')

        # validate location details
        if Provinces.objects.filter(province=data['province']).count() <= 0:
            errors.append('Incorrect province code .')
        if Districts.objects.filter(district=data['district']).count() <= 0:
            errors.append('Incorrect district code .')
        if Sectors.objects.filter(sector_code=data['sector']).count() <= 0:
            errors.append('Incorrect sector code .')
        if Cells.objects.filter(cell_code=data['cellule']).count() <= 0:
            errors.append('Incorrect cell code .')
        if Village.objects.filter(village_code=data['village']).count() <= 0:
            errors.append('Incorrect village code .')

        # validate country codes
        if Countryparam.objects.filter(country_code=data['country_code']).count() <= 0:
            errors.append('Incorrect country code .')
        if Countryparam.objects.filter(country_code=data['resident_country']).count() <= 0:
            errors.append('Incorrect resident country code .')

        if Gltitle.objects.filter(title_code__contains=data['title']).count() <= 0:
            errors.append('Invalid title code .')
            # validate address
        if len(data['address2']) > 20:
            errors.append('Address2 should have a maximum of 20 char .')

        if len(data['address3']) > 20:
            errors.append('Address3 should have a maximum of 20 char .')

        if len(data['surname']) > 40:
            errors.append('Surname should have a maximum of 40 char .')

        if len(data['other_names']) > 30:
            errors.append('Other_names should have a maximum of 30 char .')

        if len(data['contact_telephone']) > 12:
            errors.append('Contact telephone should have a maximum of 12 char .')

        if len(data['contact_position']) > 25:
            errors.append('Contact_position should have a maximum of 25 char .')

        if len(data['fax']) > 15 :
            errors.append('Fax should have a maximum of 15 char .')
            
        if len(data['telephone']) > 20 :
            errors.append('telephone should have a maximum of 20 char .')

        if len(data['mobile_no']) > 20 :
            errors.append('mobile_no should have a maximum of 20 char .')


    return errors
