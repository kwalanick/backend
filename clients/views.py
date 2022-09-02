from django.shortcuts import render,get_object_or_404
from django.contrib import messages,auth
from .models import ClientUpload ,Provinces,Districts,Sectors,Cells, Village
from uploads.models import Glclmast,BatchCode,BatchSerial,Fleetusers
from io import StringIO
import re
import csv
import datetime
from datetime import date
from datetime import datetime
date_time = date.today()
# Create your views here.
# variable declaration
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


def upload_form(request,username):
    clients = Glclmast.objects.all()

    batches = BatchCode.objects.filter(batch_type=1)
    context = {
        'username': username,
        'batches' : batches
    }
    return render(request,'client_upload.html',context)


def upload_csv(request,username):

    try:

        csv_file = request.FILES["csv_file"]
        file = csv_file.read().decode('utf-8')
        csv_data = csv.reader(StringIO(file), delimiter=',')
        new_list = []
        for row in csv_data:
            new_list.append(row)
        count = 0
        new_list.pop(0)
        print(new_list[0][0])
        errors = validate_client_list(new_list)

        if len(errors) == 0:
            batch = BatchCode.objects.create(
                batch_no=get_next_serial(),
                uploaded_by=username,
                batch_type=1
            )
            batch.save()
            upload_clients(new_list,batch.batch_no)
            messages.success(request, 'You have successfully uploaded Client details in the AIMS staging area')

        else:
            for error in errors:
                messages.error(request,error)
    except Exception as e:
        messages.error(request,e)

    batches = BatchCode.objects.filter(batch_type=1)
    context = {
        'username':username,
        'batches': batches
    }
    return render(request,'client_upload.html',context)


def batch_detail(request,batch_no,username):

    clients = ClientUpload.objects.filter(batch_no=batch_no)
    context = {
        "batch_no" : batch_no,
        "clients" : clients,
        "username" : username
    }
    return render(request,'client_details.html',context)


def upload_clients(client_list,batch_no):
    for i in range(0,len(client_list)):
        bnr_classification=client_list[i][0]
        salutation=client_list[i][1]
        surname=client_list[i][2]
        fname=client_list[i][3]
        client_name=client_list[i][4]
        nationality_code=client_list[i][5]
        residence_code=client_list[i][6]
        id_type=client_list[i][7]
        id_number=client_list[i][8]
        dob_1=client_list[i][9]
        dob=datetime.strptime(dob_1,"%d/%m/%Y")
        gender = client_list[i][10]
        marital_status = client_list[i][11]
        spouse_name = client_list[i][12]
        residence_type = client_list[i][13]
        address = client_list[i][14]
        email = client_list[i][15]
        telephone = client_list[i][16]
        fax = client_list[i][17]
        occupation_code = client_list[i][18]
        industry_code = client_list[i][19]
        economic_sub = client_list[i][20]
        relsh = client_list[i][21]

        pob_province = client_list[i][22]
        pob_district = client_list[i][23]
        pob_sector = client_list[i][24]
        pob_cell = client_list[i][25]
        pob_village = client_list[i][26]

        province = client_list[i][27]
        district = client_list[i][28]
        sector = client_list[i][29]
        cell = client_list[i][30]
        village = client_list[i][31]

        contact_person = client_list[i][32]
        contact_position = client_list[i][33]
        contact_tel = client_list[i][34]

        client = ClientUpload.objects.create(
                        bnr_classification=bnr_classification,
                        salutation = salutation,
                        sname = surname,
                        fname = fname,
                        client_name = client_name,
                        country_code = nationality_code,
                        resident_country = residence_code,
                        identity_type = id_type,
                        identity_card_no = id_number,
                        birth_date = dob,
                        gender = gender,
                        marital_status = marital_status,
                        spouse_name = spouse_name,
                        email = email,
                        mobile_no = telephone,
                        residence_type = residence_type,
                        occupation_code = occupation_code,
                        naics_code = industry_code,
                        economic_sub_sector = economic_sub,
                        relation_to_company_code = relsh,
                        pob_province = pob_province,
                        pob_district = pob_district,
                        pob_sector = pob_sector,
                        pob_cell = pob_cell,
                        pob_village = pob_village,
                        rdb_reg_no = id_number,
                        rdb_reg_date = dob,
                        province = province,
                        district = district,
                        sector = sector,
                        cell = cell,
                        village = village,
                        contact = contact_person,
                        contact_position = contact_position,
                        contact_telephone = contact_tel,
                        address = address,
                        fax=fax,
                        batch_no=batch_no
                    )
        client.save()


def validate_client_list(client_list):
    errors = []
    count = 0

    # general validation
    for i in range(0, len(client_list)):
        count += 1
        if len(client_list[i][0]) == 0:
            errors.append('Please capture the BNR Classification no at line no. ' + str(count))
        if len(client_list[i][1]) == 0:
            errors.append('Please capture the Salutation at line no. ' + str(count))
        if len(client_list[i][2]) == 0:
            errors.append('Please capture the Surname no at line no. ' + str(count))
        if len(client_list[i][3]) == 0:
            errors.append('Please capture the First Name at line no. ' + str(count))
        if len(client_list[i][4]) == 0:
            errors.append('Please capture the Client_name at line no. ' + str(count))
        if len(client_list[i][5]) == 0:
            errors.append('Please capture the Nationality_code at line no. ' + str(count))
        if len(client_list[i][6]) == 0:
            errors.append('Please capture the Residence_code at line no. ' + str(count))
        if len(client_list[i][7]) == 0:
            errors.append('Please capture the ID Type at line no. ' + str(count))
        if len(client_list[i][8]) == 0:
            errors.append('Please capture the Identity Card No No at line no. ' + str(count))
        if len(client_list[i][9]) == 0:
            errors.append('Please capture the Date of Birth at line no. ' + str(count))
        if len(client_list[i][10]) == 0:
            errors.append('Please capture the Gender at line no. ' + str(count))
        if not re.fullmatch(regex,client_list[i][15]) :
            errors.append('Please capture a valid email address at '+str(count))

        # validate admin units birth location details
        if Provinces.objects.filter(province=client_list[i][22]).count() <= 0:
            errors.append('Incorrect place of birth province code at line no.' + str(count))
        if Districts.objects.filter(district=client_list[i][23]).count() <= 0:
            errors.append('Incorrect place of birth district code at line no.' + str(count))
        if Sectors.objects.filter(sector_code=client_list[i][24]).count() <= 0:
            errors.append('Incorrect place of birth cell code at line no.' + str(count))
        if Cells.objects.filter(cell_code=client_list[i][25]).count() <= 0:
            errors.append('Incorrect place of birth cell code at line no.' + str(count))
        if Village.objects.filter(village_code=client_list[i][26]).count() <= 0:
            errors.append('Incorrect place of birth village code at line no.' + str(count))

        # location details
        if Provinces.objects.filter(province=client_list[i][27]).count() <= 0:
            errors.append('Incorrect province code at line no.' + str(count))
        if Districts.objects.filter(district=client_list[i][28]).count() <= 0:
            errors.append('Incorrect district code at line no.' + str(count))
        if Sectors.objects.filter(sector_code=client_list[i][29]).count() <= 0:
            errors.append('Incorrect sector code at line no.' + str(count))
        if Cells.objects.filter(cell_code=client_list[i][30]).count() <= 0:
            errors.append('Incorrect cell code at line no.' + str(count))
        if Village.objects.filter(village_code=client_list[i][31]).count() <= 0:
            errors.append('Incorrect village code at line no.' + str(count))

        # id number validations
        print(client_list[i][8])
        if len(client_list[i][8]) != 16 and client_list[i][0]=='001' and  client_list[i][0]=='C081':
            errors.append('Please capture ID number in the correct format')
        if str(client_list[i][8])[5] not in ['7','8']:
             errors.append('Error in ID number gender section')

        # validate Names
        if not re.match("^[A-Za-z']+$",client_list[i][2]):
            errors.append('Surname should only contain alphabetic characters '+str(count))
        if not re.match("^[A-Za-z']+$",client_list[i][3]):
            errors.append('First Name should only contain alphabetic characters '+str(count))
        if not re.match("^[A-Za-z']+\s+[A-Za-z']+$",client_list[i][4]):
            errors.append('Full Names should be alphabetic separated by a space '+str(count))

    return errors


def review_upload(request,batch_no,username):
    user_name = username.ljust(15)
    review = Fleetusers.objects.get(user_name=username)
    batch = BatchCode.objects.get(batch_no=batch_no)

    if review.review_fleet == 'Y':

        if batch.uploaded_by == username:
            batch = BatchCode.objects.get(batch_no=batch_no)
            batch.reveiwed = 'Y'
            batch.reviewed_by = user_name
            batch.reveiwed_date = date.today()
            batch.save()
            messages.success(request, 'The member upload has been reviewed successfully')
        else:
            messages.error(request,'You cannot upload and review at the same time!')

    else:
        messages.error(request,'You are not allowed to review fleet uploads')

    batches = BatchCode.objects.filter(batch_type=1)
    context = {
        "batches": batches,
        "username":username,
    }
    return render(request,'client_upload.html',context)


def process_batch(request,batch_no,username):
    try:
        batch = BatchCode.objects.get(batch_no=batch_no)
        user_name = username.ljust(15)
        process_fleet = Fleetusers.objects.get(user_name=username).process_fleet
        if batch.processed == 'N' and batch.reveiwed == 'Y' and process_fleet == 'Y':
            # get clients in the batch
            clients = ClientUpload.objects.filter(batch_no=batch_no)
            for cl in clients:
                # check if the customer exists
                client_type = 'I' if cl.bnr_classification == '001' else 'C'
                company_reg = cl.identity_card_no[0:8]
                id_unique = cl.identity_card_no[0:13]

                ##if Village.objects.filter(village_code=cl.pob_village).count() > 0:
                village_instance = Village.objects.get(village_code=cl.pob_village)

                client_count = Glclmast.objects.filter(id_unique=id_unique).count()
                if client_count == 0:
                    # add a new client
                    get_name = cl.sname if client_type=='I' else cl.client_name
                    client_number = gen_client_num(get_name)
                    print('Adding new ............ ',client_number)
                    new_client = Glclmast.objects.create(
                        client_no=client_number,
                        bnr_classification=cl.bnr_classification,
                        title=cl.salutation,
                        surname=cl.sname,
                        other_names=cl.fname,
                        name=str(cl.client_name).ljust(200,' '),
                        resident_country=cl.resident_country,
                        country_code=cl.country_code,
                        identity_card_no=cl.identity_card_no,
                        id_doc=cl.identity_type,
                        marital_status=cl.marital_status,
                        birth_date=cl.birth_date,
                        gender=cl.gender,
                        id_unique=id_unique,
                        spourse_name=cl.spouse_name,
                        residence_type=cl.residence_type,
                        email=cl.email,
                        mobile_no=cl.mobile_no,
                        telephone=cl.mobile_no,
                        fax=cl.fax,
                        occupation=cl.occupation_code,
                        naics_code=cl.naics_code,
                        economic_sub_sector=cl.economic_sub_sector,
                        relation_to_company_code=cl.relation_to_company_code,
                        rdb_reg_no=company_reg,
                        rdb_reg_date=cl.rdb_reg_date,
                        tin_no=company_reg,
                        contact=cl.contact,
                        contact_position=cl.contact_position,
                        contact_telephone=cl.contact_telephone,
                        province=cl.province,
                        district=cl.district,
                        sector=cl.sector,
                        cellule=cl.cell,
                        village=cl.village,
                        birth_reg_village=cl.pob_village,
                        client_type=client_type,
                        batch_no=cl.batch_no,
                    )
                    #new_client.save()
                else:
                    # edit client information from the system
                    id_unique = cl.identity_card_no[0:13]
                    print(cl.identity_card_no)
                    #client = Glclmast.objects.get(identity_card_no=cl.identity_card_no)
                    client_edit = Glclmast.objects.filter(id_unique = id_unique).update(
                        bnr_classification=cl.bnr_classification,
                        title=cl.salutation,
                        surname=cl.sname,
                        other_names=cl.fname,
                        name=str(cl.client_name).ljust(200,' '),
                        resident_country=cl.resident_country,
                        country_code=cl.country_code,
                        identity_card_no=cl.identity_card_no,
                        id_doc=cl.identity_type,
                        marital_status=cl.marital_status,
                        birth_date=cl.birth_date,
                        gender=cl.gender,
                        id_unique=id_unique,
                        spourse_name=cl.spouse_name,
                        residence_type=cl.residence_type,
                        email=cl.email,
                        mobile_no=cl.mobile_no,
                        telephone=cl.mobile_no,
                        fax=cl.fax,
                        occupation=cl.occupation_code,
                        naics_code=cl.naics_code,
                        economic_sub_sector=cl.economic_sub_sector,
                        relation_to_company_code=cl.relation_to_company_code,
                        rdb_reg_no=company_reg,
                        rdb_reg_date=cl.rdb_reg_date,
                        tin_no=company_reg,
                        contact=cl.contact,
                        contact_position=cl.contact_position,
                        contact_telephone=cl.contact_telephone,
                        province=cl.province,
                        district=cl.district,
                        sector=cl.sector,
                        cellule=cl.cell,
                        village=cl.village,
                        birth_reg_village=cl.pob_village,
                        client_type=client_type,
                        batch_no=cl.batch_no,
                    )
                    #client_edit.save()

            client_count = Glclmast.objects.filter(batch_no=batch_no).count()
            temp_count = ClientUpload.objects.filter(batch_no=batch_no).count()

            print(f"Compare records updated in both files {client_count} -  {temp_count}")

            if temp_count == client_count:
                batch.processed = 'Y'
                batch.processed_by = username
                batch.save()
                messages.success(request, 'You have successfully updated the batch.')
            else:
                messages.error(request, 'Batch processing failed !!!')

        elif batch.reveiwed != 'Y':
            messages.error(request, 'The batch has not yet been reviewed')
        elif process_fleet != 'Y':
            messages.error(request, 'You are not allowed to process upload.')
        else:
            messages.error(request,'The batch has already been processed !')

    except Exception as e:
        messages.error(request,e)

    batches = BatchCode.objects.filter(batch_type=1)
    context = {
        'batch_no': batch_no,
        'username': username,
        'batches': batches
    }
    return render(request,'client_upload.html',context)


def gen_client_num(firstName):
    next_serial = Glclmast.objects.filter(surname__startswith=firstName[:2]).count() + 1
    client_number = firstName[:2].upper() + format(next_serial, '06')
    return client_number


def get_next_serial():
    serial = BatchSerial.objects.get(id=1)
    batch_no = 'CL' + format(serial.serial_no, '06')
    serial.serial_no = serial.serial_no + 1
    serial.save()
    return batch_no


