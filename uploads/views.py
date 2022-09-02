from django.shortcuts import render
from django.http.response import HttpResponse
from django.contrib import messages,auth
from django.shortcuts import render , redirect,get_object_or_404
from .models import BatchCode , BatchSerial ,Memberupd ,MemberupdNew,Fleetusers,Schememaster,\
    Membermaster,Glclmast,Glmmridtl,Glriders,Glrdrate,Glrates,Glmploan,Premrates,Glscheme,Glmmast,Maxserials
from io import StringIO
import re
import csv
import datetime
from datetime import datetime, date
date_time = date.today()
# Create your views here.


def test_project(request):
    return render(request,'base.html')


def upload_form(request,user_id):
    batches = BatchCode.objects.filter(batch_type=2)
    context = {
        'batches': batches,
        'policy_no': '100100162',
        'username': user_id
    }
    return render(request,'uploadForm.html',context)



def batch_detail(request,batch_no,username):
    #print(endt_renewal_no)
    members = MemberupdNew.objects.filter(batch_no=batch_no)
    context = {
        #"endt_renewal_no" : endt_renewal_no,
        "batch_no" : batch_no,
        "members" : members,
        "username" : username
    }
    return render(request,'batch_details.html',context)


def upload_csv(request,username):
    try:
        print('TESTING UPLOAD !!')
        csv_file = request.FILES["csv_file"]
        file = csv_file.read().decode('utf-8')
        csv_data = csv.reader(StringIO(file), delimiter=',')
        new_list = []
        for row in csv_data:
            new_list.append(row)
        count = 0
        new_list.pop(0)
        print(new_list[0][0])
        # get policy_no
        w_policy_no=new_list[0][0]

        errors = validate_member_list(new_list)
        if len(errors) == 0 :
            batch = BatchCode.objects.create(
                batch_no = get_next_serial(),
                policy_no = w_policy_no,
                uploaded_by = username,
                batch_type=2
            )
            batch.save()

            totals = upload_members(new_list,batch)

            updateBatch = BatchCode.objects.get(batch_no=batch)
            updateBatch.premium_total = totals[0]
            updateBatch.sum_total = totals[1]
            updateBatch.save()
            print("No errors in the file !!!!")
            messages.success(request, 'You have successfully uploaded Member details in the AIMS staging area')

        else:
            for error in errors:
                messages.error(request,error)

    except Exception as e:
        messages.error(request,e)

    batches = BatchCode.objects.filter(batch_type=2)
    context = {

        "batches": batches,
        "username": 'nndehi'
    }
    return render(request,'uploadForm.html',context)


def upload_members(new_list,batch):
    count = 0
    w_sum = 0
    w_prem = 0

    for i in range(0,len(new_list)):
        count +=1
        print(f"Uploading members information record - {count}")
        policy_no = new_list[i][0]
        id_number_1 = (new_list[i][1])
        id_number = id_number_1[0:16]
        first_name = str(new_list[i][2]).upper()
        surname = str(new_list[i][3]).upper()
        full_names = str(new_list[i][4]).upper()
        dob_1 = new_list[i][5]
        dob = datetime.strptime(dob_1,"%d/%m/%Y")
        birth_year = new_list[i][6]
        age = new_list[i][7]
        monthly_salary = new_list[i][8]
        annual_salary = new_list[i][9]

        death_sum = new_list[i][10]
        partial_sum = new_list[i][11]
        loss_of_income = new_list[i][12]
        dreaded_diseases_sum = new_list[i][13]
        fun_fees_staff_sum = new_list[i][14]
        fun_fees_legal_sum = new_list[i][15]
        fun_fees_dep_sum = new_list[i][16]
        medical_sum = new_list[i][17]

        death_prem = new_list[i][18]
        partial_prem = new_list[i][19]
        loss_of_income_prem = new_list[i][20]
        dreaded_diseases_prem = new_list[i][21]
        fun_fees_staff_prem = new_list[i][22]
        fun_fees_legal_prem = new_list[i][23]
        fun_fees_dep_prem = new_list[i][24]
        medical_prem = new_list[i][25]
        total_prem = new_list[i][26]
        prorated_prem = new_list[i][27]

        join_date_1 = new_list[i][28]
        join_date = datetime.strptime(join_date_1,"%d/%m/%Y")
        join_year = datetime.strptime(join_date_1,"%d/%m/%Y").year
        expiry_date_1 = new_list[i][29]
        expiry_date = datetime.strptime(expiry_date_1,"%d/%m/%Y")


        commence_date = datetime.strptime(new_list[i][30],"%d/%m/%Y")
        loan_period = new_list[i][31]
        interest_basis = new_list[i][32]
        interest_rate = new_list[i][33]
        loan_amount = float(new_list[i][34])
        if loan_amount > 0:
            death_sum = loan_amount
        admin_fee = new_list[i][35]
        vat = new_list[i][36]
        retrenchment = new_list[i][37]
        retrench_period = new_list[i][38]

        branch = new_list[i][39]
        id_type = new_list[i][40]

        w_age = calculateAge(dob)

        if MemberupdNew.objects.filter(id_number=id_number,batch_no=batch.batch_no,commence_date=commence_date).count() == 0:
            member = MemberupdNew.objects.create(
                policy_no=policy_no,
                id_number=id_number_1,
                fname=remove_accents(first_name),
                lname=remove_accents(surname),
                surname=remove_accents(surname),
                full_name=remove_accents(full_names),
                date_of_birth=dob,
                birth_year=birth_year,
                age=age,
                monthly_sal=monthly_salary,
                annual_sal=annual_salary,
                death_sum=death_sum,
                partial_sum=partial_sum,
                loss_income_sum=loss_of_income,
                dread_disease_sum=dreaded_diseases_sum,
                fun_fees_staff_sum=fun_fees_staff_sum,
                fun_fees_legal_sum=fun_fees_legal_sum,
                medical_sum=medical_sum,
                death_prem=death_prem,
                partial_prem=partial_prem,
                loss_of_income_prem=loss_of_income_prem,
                dread_diseases_prem=dreaded_diseases_prem,
                fun_fees_staff_prem=fun_fees_staff_prem,
                fun_fees_legal_prem=fun_fees_legal_prem,
                medical_prem=medical_prem,
                total_premium=total_prem,
                batch_no=batch,
                join_date=join_date,
                expiry_date=expiry_date,
                fun_fees_dep_sum=fun_fees_dep_sum,
                fun_fees_dep_prem=fun_fees_dep_prem,
                prorated_prem=prorated_prem,
                commence_date=commence_date,
                loan_period=loan_period,
                interest_basis=interest_basis,
                interest_rate=interest_rate,
                loan_amount=loan_amount,
                admin_fee=admin_fee,
                vat=vat,
                retrenchment=retrenchment,
                branch=branch,
                id_type=id_type,
                retrench_period=retrench_period,
                uw_year = join_year,
                processed_flag='N'
            )
        else:
            member = MemberupdNew.objects.filter(id_number=id_number,batch_no=batch.batch_no,commence_date=commence_date).update(
                policy_no=policy_no,
                id_number=id_number_1,
                fname=remove_accents(first_name),
                lname=remove_accents(surname),
                surname=remove_accents(surname),
                full_name=remove_accents(full_names),
                date_of_birth=dob,
                birth_year=birth_year,
                age=age,
                monthly_sal=monthly_salary,
                annual_sal=annual_salary,
                death_sum=death_sum,
                partial_sum=partial_sum,
                loss_income_sum=loss_of_income,
                dread_disease_sum=dreaded_diseases_sum,
                fun_fees_staff_sum=fun_fees_staff_sum,
                fun_fees_legal_sum=fun_fees_legal_sum,
                medical_sum=medical_sum,
                death_prem=death_prem,
                partial_prem=partial_prem,
                loss_of_income_prem=loss_of_income_prem,
                dread_diseases_prem=dreaded_diseases_prem,
                fun_fees_staff_prem=fun_fees_staff_prem,
                fun_fees_legal_prem=fun_fees_legal_prem,
                medical_prem=medical_prem,
                total_premium=total_prem,
                batch_no=batch,
                join_date=join_date,
                expiry_date=expiry_date,
                fun_fees_dep_sum=fun_fees_dep_sum,
                fun_fees_dep_prem=fun_fees_dep_prem,
                prorated_prem=prorated_prem,
                commence_date=commence_date,
                loan_period=loan_period,
                interest_basis=interest_basis,
                interest_rate=interest_rate,
                loan_amount=loan_amount,
                admin_fee=admin_fee,
                vat=vat,
                retrenchment=retrenchment,
                branch=branch,
                id_type=id_type,
                retrench_period=retrench_period,
                uw_year=join_year,
                processed_flag='N'
            )
        w_prem += float(total_prem)
        w_sum += float(death_sum)

    return [w_prem,w_sum]


def validate_member_list(member_list):
    count = 0
    errors = []
    # general validation
    for i in range(0,len(member_list)):
        count +=1
        if len(member_list[i][0]) == 0:
            errors.append('Please capture the policy no at line no. '+str(count))
        if Schememaster.objects.filter(policy_no=str(member_list[i][0]).strip()).count() <= 0:
            errors.append(f"The policy no does not exist in AIMS APPLICATION - {member_list[i][0]} at line {count}")
        if len(member_list[i][1]) == 0:
            errors.append('Please capture the id number at line no. '+str(count))
        if len(member_list[i][1]) != 16 and member_list[i][40] == 2 :
            errors.append('Please capture ID number in the correct format')
        if str(member_list[i][1]) not in ['7', '8'] and member_list[i][40] == 2:
            errors.append('Error in ID number gender section')
        if len(member_list[i][40]) == 0:
            errors.append('Identity type should not be null')
        if len(member_list[i][2]) == 0:
            errors.append('Please capture the first name no at line no. '+str(count))
        if len(member_list[i][3]) == 0:
            errors.append('Please capture the surname no at line no. '+str(count))
        if len(member_list[i][4]) == 0:
            errors.append('Please capture the date of Birth at line no. '+str(count))

    return errors


def process_batch(request,batch_no,policy_no,username):

    try:
        batch = BatchCode.objects.get(batch_no=batch_no)
        user_name = username.ljust(15)
        process_fleet = Fleetusers.objects.get(user_name=username).process_fleet
        if batch.processed == 'N' and batch.reveiwed =='Y' and process_fleet == 'Y':

            # check if the scheme exists
            polm = get_object_or_404(Schememaster, policy_no=policy_no)
            print(polm.policy_no)

            w_total = MemberupdNew.objects.filter(batch_no=batch_no).count()
            w_count = 0

            if polm.policy_no:
                # print(f"Batch No  {batch_no} ")
                id_no = '1197180031141080¿'.ljust(17,' ')
                members = MemberupdNew.objects.filter(batch_no=batch_no ,processed_flag='N')
                # members = MemberupdNew.objects.filter(pk=555246)
                count = 0
                w_total = MemberupdNew.objects.filter(batch_no=batch_no).count()
                w_count = 0

                for mem_rec in members:
                    # check if client number exists in GLCLMAST
                    id_unique = ''
                    client_count = 0

                    id_unique = mem_rec.id_number[0:13] if (mem_rec.id_type == 2) else mem_rec.id_number[0:13].strip()
                    scheme = Schememaster.objects.get(policy_no=mem_rec.policy_no)
                    # print(f"Get Policy - {scheme.policy_no}")
                    # add_scheme(scheme,mem_rec)

                    # print(f"ID unique check -{mem_rec.id_number} --- {id_unique}--")
                    # create new client
                    id_no = re.sub('¿', '', id_unique).ljust(13, ' ')
                    client_count = Glclmast.objects.filter(id_unique=id_no).count()
                    # print(f"Client count - {client_count}")
                    if client_count == 0:
                        # print("Creating a new client ")
                        client_number = gen_client_num(mem_rec.surname)
                        print(f"Check client now - {mem_rec.surname} ---- {client_number}")
                        client_new = Glclmast.objects.create(
                            client_no=client_number,
                            client_type='I',
                            surname=mem_rec.surname,
                            other_names=mem_rec.fname,
                            name=str(mem_rec.full_name).ljust(200,' '),
                            birth_date = mem_rec.date_of_birth,
                            identity_card_no=re.sub('¿','',str(mem_rec.id_number)[0:16]),
                            id_unique=re.sub('¿', '', id_unique),
                            identity_type=mem_rec.id_type,
                            creation_date=date_time,
                            batch_no=batch_no
                        )
                        # client.save()
                        id_no = re.sub('¿','',id_unique).ljust(13,' ')
                        client = Glclmast.objects.get(id_unique=id_no)
                        print(f"Client No generated - {client.client_no} -- {mem_rec.full_name} -- count {count}")
                    else:
                        # get client number from GLCLMAST
                        id_unique=mem_rec.id_number[0:13]
                        # print(mem_rec.id_number)
                        # print("Editing a new client ")
                        client_edit = Glclmast.objects.filter(id_unique__contains = id_unique).update(
                            client_type='I',
                            surname=str(mem_rec.surname).upper(),
                            other_names=mem_rec.fname,
                            name=str(mem_rec.full_name).ljust(200,' '),
                            birth_date=mem_rec.date_of_birth,
                            identity_card_no=re.sub('¿','',str(mem_rec.id_number)[0:16]),
                            #id_unique=re.sub('¿','',id_unique),
                            identity_type=mem_rec.id_type,
                            batch_no=batch_no
                        )
                        id_no = re.sub('¿','',id_unique).ljust(13,' ')
                        client = Glclmast.objects.get(id_unique = id_no)
                        print(f"Client No edited - {client.client_no} -- {mem_rec.full_name} -- count {count}")
                    count += 1

                    add_member(client,mem_rec,mem_rec.policy_no,batch_no)
                    update_temp = MemberupdNew.objects.filter(pk=mem_rec.pk).update(
                        processed_flag='Y'
                    )
                    w_count = w_count + 1
            else:
                messages.error(request,'Create the scheme in AIMS first before uploading members')
                
              
            w_count = MemberupdNew.objects.filter(batch_no=batch_no).count()
            w_total = MemberupdNew.objects.filter(batch_no=batch_no,processed_flag='Y').count()
            # print(f"Batch process Comparison =>  All -  {w_count}  - Processed - {w_total}")  
            if w_count == w_total:
                batch.processed = 'Y'
                batch.processed_by = username
                batch.save()
                messages.success(request, 'You have successfully updated the batch.')
            else:
                messages.error(request,'Batch processing failed !!!')

        elif batch.reveiwed != 'Y':
            messages.error(request, 'The batch has not yet been reviewed')
        elif process_fleet != 'Y':
            messages.error(request, 'You are not allowed to process upload.')
        else:
            messages.error(request,'The batch has already been processed !')

    except Exception as e:
        messages.error(e)

    batches = BatchCode.objects.filter(policy_no=policy_no,batch_type=2)
    context = {
        'batches':batches,
        'policy_no':policy_no,
        'username': username
    }
    return render(request,'uploadForm.html',context)


def add_scheme(scheme,mem_rec):
    if Glscheme.objects.filter(policy_no=scheme.policy_no,client_no=scheme.client_no,uw_year=mem_rec.uw_year).count() == 0:
        new_scheme = Glscheme.objects.create(
            policy_no=scheme.policy_no,
            client_no=scheme.client_no,
            uw_year=mem_rec.uw_year,
            scheme_name=scheme.scheme_name,
            #commence_year=scheme.commence_year,
            #commence_month=scheme.commence_month,
            #commence_day=scheme.commence_day,
            free_cover_limit=scheme.free_cover_limit,
            branch=scheme.branch,
            agent=scheme.agent,
            #pay_freq_ta=scheme.pay_freq_ta

        )
    else:
        edit_scheme = Glscheme.objects.filter(policy_no=scheme.policy_no,client_no=scheme.client_no,uw_year=mem_rec.uw_year).update(
            policy_no=scheme.policy_no,
            client_no=scheme.client_no,
            uw_year=mem_rec.uw_year,
            #commence_year=scheme.commence_year,
            #commence_month=scheme.commence_month,
            #commence_day=scheme.commence_day,
            free_cover_limit=scheme.free_cover_limit,
            branch=scheme.branch,
            agent=scheme.agent,
            #pay_freq_ta=scheme.pay_freq_ta
        )


def add_member(client,mem_rec,policy_no,batch_no):
    # intialize computation variables
    rider_prem = 0
    rider_sum = 0
    comm_amount = 0
    comm_rate = 0
    member_no = 0
    scheme = Schememaster.objects.get(policy_no=policy_no)
    #member_count = Membermaster.objects.filter(policy_no=policy_no).count()
    rider_sum = mem_rec.partial_sum+mem_rec.loss_income_sum+mem_rec.dread_disease_sum+\
                mem_rec.fun_fees_legal_sum+mem_rec.fun_fees_staff_sum+mem_rec.medical_sum+mem_rec.fun_fees_dep_sum
    rider_prem = mem_rec.partial_prem+mem_rec.loss_of_income_prem+mem_rec.dread_diseases_prem+\
                    mem_rec.fun_fees_staff_prem+mem_rec.fun_fees_legal_prem+mem_rec.medical_prem+mem_rec.fun_fees_dep_prem

    # compute commissions
    if scheme.commission_rate is None:
        comm_amount = 0
        comm_rate = 0
    else:
        # print('Check comm rate !!')
        comm_amount = 0 #(float(scheme.commission_rate) / 100) * mem_rec.total_premium
        comm_rate = scheme.commission_rate

    # get premium rate
    if Glrates.objects.filter(age=mem_rec.age).count() > 0:
        w_rate = Glrates.objects.get(age=mem_rec.age).ind_rate
    else:
        w_rate = 0

    if Membermaster.objects.filter(policy_no=policy_no,client_no=client.client_no).count() == 0:
        # get member no
        members = Membermaster.objects.filter(policy_no=policy_no)
        member_serials = [num.member_no for num in members]
        if len(member_serials) == 0:
            member_no = 1
        else:
            member_no = max(member_serials) + 1
        # print(f"Generated Member No {policy_no} ---  {member_no}")
        # create member in Membermaster
        member = Membermaster.objects.create(
            member_no=member_no,
            policy_no=policy_no,
            client_no=client.client_no,
            first_name=mem_rec.fname,
            surname=mem_rec.surname,
            other_names=mem_rec.fname,
            name=str(mem_rec.full_name).ljust(200,' ').strip(),
            age=mem_rec.age,
            dob=mem_rec.date_of_birth,
            current_salary=mem_rec.annual_sal,
            annual_salary=mem_rec.annual_sal,
            total_sum_assured=mem_rec.death_sum,
            lc_total_annual_prem=mem_rec.total_premium,
            lc_norm_annual_prem=mem_rec.total_premium,
            batch_no=batch_no,
            rider_premium=rider_prem,
            rider_benefit=rider_sum,
            status_code=1,
            join_date=mem_rec.join_date,
            period_from=mem_rec.join_date,
            period_to=mem_rec.expiry_date,
            uw_year=mem_rec.uw_year,
            lc_cover_factor=scheme.lc_factor,
            comm_rate=comm_rate,
            comm_amount=comm_amount,
            type_of_bus=1,
            co_insure='N',
            company_share=100,
            premium_rate=w_rate,
            est_loan_amount=mem_rec.loan_amount,
            retrenchment=mem_rec.retrenchment,
            retrench_period=mem_rec.retrench_period,
            branch=mem_rec.branch,
            created_date=date_time
        )
        add_memberhist(member)
        #set_riders(mem_rec, member_no, scheme.uw_year, batch_no)
        member_instance = Membermaster.objects.get(policy_no=policy_no, client_no=client.client_no)
        if scheme.scheme_type in ['100']:
            loan_no = 0
            set_riders(mem_rec, member_instance.member_no, scheme.uw_year, batch_no,loan_no)
        if scheme.scheme_type in ['700', '800']:
            add_loan(member_instance, mem_rec)
    else:

        # edit member in Membermaster
        # print("Editing member information in the scheme !!  ", client.client_no)
        edit_member = Membermaster.objects.filter(policy_no=policy_no, client_no=client.client_no).update(
            first_name=mem_rec.fname,
            surname=mem_rec.surname,
            other_names = mem_rec.fname,
            name=str(mem_rec.full_name).ljust(200,' ').strip(),
            age=mem_rec.age,
            dob=mem_rec.date_of_birth,
            current_salary=mem_rec.annual_sal,
            annual_salary=mem_rec.annual_sal,
            total_sum_assured=mem_rec.death_sum,
            lc_total_annual_prem=mem_rec.total_premium,
            lc_norm_annual_prem=mem_rec.total_premium,
            batch_no=batch_no,
            status_code=1,
            rider_premium=rider_prem,
            rider_benefit=rider_sum,
            join_date=mem_rec.join_date,
            period_from=mem_rec.join_date,
            period_to=mem_rec.expiry_date,
            uw_year=mem_rec.uw_year,
            lc_cover_factor=scheme.lc_factor,
            comm_rate=comm_rate,
            comm_amount=comm_amount,
            type_of_bus=1,
            co_insure='N',
            company_share=100,
            premium_rate=w_rate,
            est_loan_amount=mem_rec.loan_amount,
            retrenchment=mem_rec.retrenchment,
            retrench_period=mem_rec.retrench_period,
            branch=mem_rec.branch
        )
        # get member instance

        member_instance = Membermaster.objects.get(policy_no=policy_no, client_no=client.client_no)
        add_memberhist(member_instance)
        if scheme.scheme_type in ['100']:
            loan_no = 0
            set_riders(mem_rec, member_instance.member_no, scheme.uw_year, batch_no,loan_no)
        if scheme.scheme_type in ['700', '800']:
            add_loan(member_instance, mem_rec)


def add_memberhist(member):
    #print(f"Adding in glmmast ...{member.policy_no} - {member.client_no} - {member.member_no} - {member.uw_year}")
    #print(f"Check scheme Type {str(member.policy_no)[0:3]}")

    if Glmmast.objects.filter(policy_no=member.policy_no,client_no=member.client_no,uw_year=member.uw_year).count() == 0:
        member_hist = Glmmast.objects.create(
            policy_no=member.policy_no,
            client_no=member.client_no,
            member_no=member.member_no,
            uw_year=member.uw_year,
            total_sum_assured=member.total_sum_assured,
            lc_norm_annual_prem=member.lc_norm_annual_prem,
            lc_total_annual_prem=member.lc_norm_annual_prem,
            rider_premium=member.rider_premium,
            rider_benefit=member.rider_benefit,
            surname=str(member.surname).strip(),
            other_names=str(member.other_names).strip(),
            age=member.age,
            date_joined=member.join_date,
            comm_amount=member.comm_amount,
            retrench_period=member.retrench_period,
            retrenchment=member.retrenchment,
            period_from=member.period_from,
            comm_rate=member.comm_rate,
            batch_no=member.batch_no,
            status=member.status_code,
            sex=member.gender,
            scheme_type=str(member.policy_no)[0:3],
            uw_date=date_time,
            start_date=member.join_date,
            annual_prem_rate=member.premium_rate,
            commence_day=member.join_date.day,
            commence_month=member.join_date.month,
            commence_year=member.join_date.year,

        )
    else:
        Glmmast.objects.filter(policy_no=member.policy_no,client_no=member.client_no,uw_year=member.uw_year).update(
            #policy_no=member.policy_no,
            #client_no=member.client_no,
            #member_no=member.member_no,
            #uw_year=member.uw_year,
            total_sum_assured=member.total_sum_assured,
            lc_norm_annual_prem=member.lc_norm_annual_prem,
            lc_total_annual_prem=member.lc_norm_annual_prem,
            rider_premium=member.rider_premium,
            rider_benefit=member.rider_benefit,
            surname=str(member.surname).strip(),
            other_names=str(member.other_names).strip(),
            age=member.age,
            date_joined=member.join_date,
            comm_amount=member.comm_amount,
            retrench_period=member.retrench_period,
            retrenchment=member.retrenchment,
            period_from=member.period_from,
            comm_rate=member.comm_rate,
            batch_no=member.batch_no,
            status=member.status_code,
            sex=member.gender,
            scheme_type=str(member.policy_no)[0:3],
            uw_date=date_time,
            start_date=member.join_date,
            annual_prem_rate=member.premium_rate,
            commence_day=member.join_date.day,
            commence_month=member.join_date.month,
            commence_year=member.join_date.year,
        )


def add_loan(member,mem_rec):
    # check if loan exists
    loan_count = 0
    loan_count = Glmploan.objects.filter(policy_no=member.policy_no,
                                         client_no=member.client_no,
                                         uw_year=member.uw_year,
                                         member_no=member.member_no,
                                         commence_date=mem_rec.commence_date,
                                         total_sum_assured=mem_rec.loan_amount
                                         ).count()
    # generate loan number
    loan_no = loan_count+1
    w_bank = Schememaster.objects.get(policy_no=mem_rec.policy_no).bank_code
    redemption_date = addYears(mem_rec.commence_date,mem_rec.loan_period)
    if Premrates.objects.filter(bank_code=w_bank,age=mem_rec.age,loan_term=mem_rec.loan_period).count() > 0:
        w_prem_rate = Premrates.objects.get(bank_code=w_bank,age=mem_rec.age,loan_term=mem_rec.loan_period).premium_rate
    else:
        w_prem_rate = 0

    if Glmploan.objects.filter(policy_no=member.policy_no,
                               client_no=member.client_no,                               
                               member_no=member.member_no                               
                               ).count() == 0 :
        loan = Glmploan.objects.create(
            policy_no=member.policy_no,
            member_no=member.member_no,
            uw_year=member.uw_year,
            client_no=member.client_no,
            loan_no=loan_no,
            commence_date=mem_rec.commence_date,
            term_years=int(mem_rec.loan_period / 12),
            term_months=mem_rec.loan_period,
            interest_basis=mem_rec.interest_basis,
            interest_rate=mem_rec.interest_rate,
            total_sum_assured=mem_rec.loan_amount,
            admin_charge=mem_rec.admin_fee,
            redemtion_date=mem_rec.expiry_date,
            prorated_prem=mem_rec.prorated_prem,
            annual_prem_rate=w_prem_rate,
            lc_norm_annual_prem=mem_rec.total_premium,
            loan_premium=mem_rec.prorated_prem,
            rider_benefit=member.rider_benefit,
            rider_premium=member.rider_premium,
            batch_no=member.batch_no
        )
        #loan.save()
        set_riders(mem_rec, member.member_no, member.uw_year, member.batch_no,loan_no)
    else:
        loan = Glmploan.objects.filter(policy_no=member.policy_no,
                                       client_no=member.client_no,
                                       uw_year=member.uw_year,
                                       member_no=member.member_no,
                                       term_months=mem_rec.loan_period,
                                       commence_date=mem_rec.commence_date
                                       ).update(
            policy_no=member.policy_no,
            member_no=member.member_no,
            uw_year=member.uw_year,
            client_no=member.client_no,
            commence_date=mem_rec.commence_date,
            term_years=int(mem_rec.loan_period / 12),
            term_months=mem_rec.loan_period,
            interest_basis=mem_rec.interest_basis,
            interest_rate=mem_rec.interest_rate,
            total_sum_assured=mem_rec.loan_amount,
            admin_charge=mem_rec.admin_fee,
            redemtion_date=mem_rec.expiry_date,
            prorated_prem=mem_rec.prorated_prem,
            annual_prem_rate=w_prem_rate,
            lc_norm_annual_prem=mem_rec.total_premium,
            loan_premium=mem_rec.prorated_prem,
            rider_benefit=member.rider_benefit,
            rider_premium=member.rider_premium,
            batch_no=member.batch_no
        )
        #loan.save()
        set_riders(mem_rec, member.member_no, member.uw_year, member.batch_no,loan_no)


def set_riders(mem_rec,member_no,uw_year,batch_no,loan_no):
    if mem_rec.fun_fees_legal_prem > 0 or not None:
        add_riders(mem_rec.policy_no, member_no, uw_year, 1, mem_rec.fun_fees_legal_prem, mem_rec.fun_fees_legal_sum,batch_no, mem_rec.age,loan_no)
    if mem_rec.dread_diseases_prem > 0 or not None:
        add_riders(mem_rec.policy_no,member_no,uw_year,2,mem_rec.dread_diseases_prem,mem_rec.dread_disease_sum,batch_no,mem_rec.age,loan_no)
    if mem_rec.loss_of_income_prem > 0 or not None:
        add_riders(mem_rec.policy_no,member_no,uw_year,3,mem_rec.loss_of_income_prem,mem_rec.loss_income_sum,batch_no,mem_rec.age,loan_no)
    if mem_rec.partial_prem > 0 or not None:
        add_riders(mem_rec.policy_no,member_no,uw_year,4,mem_rec.partial_prem,mem_rec.partial_sum,batch_no,mem_rec.age,loan_no)
    if mem_rec.fun_fees_staff_prem > 0 or not None:
        add_riders(mem_rec.policy_no,member_no,uw_year,5,mem_rec.fun_fees_staff_prem,mem_rec.fun_fees_staff_sum,batch_no,mem_rec.age,loan_no)
    if mem_rec.medical_prem > 0 or not None:
        add_riders(mem_rec.policy_no,member_no,uw_year,7,mem_rec.medical_prem,mem_rec.medical_sum,batch_no,mem_rec.age,loan_no)
    if mem_rec.fun_fees_dep_prem > 0 or not None:
        add_riders(mem_rec.policy_no,member_no,uw_year,8,mem_rec.fun_fees_dep_prem,mem_rec.fun_fees_dep_sum,batch_no,mem_rec.age,loan_no)


def add_riders(policy_no,member_no,uw_year,rider_code,rider_prem,rider_benefit,batch_no,age,loan_no):
    # check if the rider exist
    # print(f"In riders Check !!   {rider_code}")
    rider_count = Glmmridtl.objects.filter(policy_no=policy_no,member_no=member_no,uw_year=uw_year,rider_code=rider_code,loan_no=loan_no).count()

    if Glrdrate.objects.filter(rider_code=rider_code,age=age).count() >  0:
        w_rider_rate = Glrdrate.objects.get(rider_code=rider_code,age=age).rate
    else:
        w_rider_rate = 0
    # new rider
    if rider_count == 0:
        rider = Glmmridtl.objects.create(
            policy_no=policy_no,
            uw_year=uw_year,
            member_no=member_no,
            rider_code=rider_code,
            benefit=rider_benefit,
            premium = rider_prem,
            batch_no=batch_no,
            age=age,
            rate=w_rider_rate,
            loan_no=loan_no
        )
        #rider.save()
    else:
        # edit existing rider information
        rider = Glmmridtl.objects.filter(policy_no=policy_no,member_no=member_no,uw_year=uw_year,rider_code=rider_code,loan_no=loan_no).update(
            policy_no=policy_no,
            uw_year=uw_year,
            member_no=member_no,
            rider_code=rider_code,
            benefit=rider_benefit,
            premium=rider_prem,
            batch_no=batch_no,
            age=age,
            rate=w_rider_rate,
            loan_no=loan_no
        )
        #rider.save()


def validate_id_number(id_number):
    errors = []

    if len(id_number) < 16:
        errors.append('The ID Number should not less than 16 characters')

    if id_number[5] not in('8','7'):
        errors.append('The ID Number has an invalid gender section ')


def review_upload(request,batch_no,policy_no,username):
    user_name = username.ljust(15)
    # print(f"Policy No -> {policy_no} - Batch No - {batch_no}  - username -> {username}")
    review = Fleetusers.objects.get(user_name=username)
    batch = BatchCode.objects.get(batch_no=batch_no)
    # print(f"Policy No -> {batch.uploaded_by} - Review -> {username}")

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

    batches = BatchCode.objects.filter(batch_type=2).order_by('-batch_no')
    context = {
        "batches": batches,
        "policy_no": policy_no,
        "username":username
    }
    return render(request,'uploadForm.html',context)

def get_next_serial():
    serial = BatchSerial.objects.get(id=1)
    batch_no = 'BA' + format(serial.serial_no, '06')
    serial.serial_no = serial.serial_no + 1
    serial.save()
    return batch_no


def gen_client_num(firstName):
    next_serial = 0
    if Maxserials.objects.filter(starts_with__contains=str(firstName[:2])).count() > 0:
        next_serial = int(Maxserials.objects.get(starts_with__contains=str(firstName[:2])).max_serail) + 1
    else:
        next_serial = 1

    client_number = str(firstName[:2]).upper() + format(next_serial, '06')

    return client_number

import unicodedata

def remove_accents(text):    
    text = unicodedata.normalize('NFKD', text)
    return "".join([c for c in text if not unicodedata.combining(c)])



def calculateAge(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def addYears(d, years):
    try:
        #Return same day of the current year
        return d.replace(year = d.year + years)
    except ValueError:
        #If not same day, it will return other, i.e.  February 29 to March 1 etc.
        return d + (date(d.year + years, 1, 1) - date(d.year, 1, 1))

