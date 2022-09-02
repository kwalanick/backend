from django.shortcuts import render
from .models import Fobatch , Bankstateovpload , Batchcode ,Corpmonth,Lapro,Lapol,Bankstatedtl
from django.contrib import messages, auth
from django.views.decorators.csrf import csrf_exempt

import csv
import json

from io import StringIO
import datetime
from decimal import Decimal
from django.http import JsonResponse
from datetime import datetime, date
date_time = date.today()
# Create your views here.
from .tasks import my_task ,validate_fin_data_new,loop,update_bankstate
from celery.result import AsyncResult

@csrf_exempt
def upload_data(request):
    fin_data = request.POST.get('fin_data')
    username = request.POST.get('username')
    data = json.loads(fin_data)


    task = update_bankstate.delay(data,username)

    return JsonResponse({"task_id": task.id}, status=202)


def home(request,username):
    context = {
        'username': username
    }
    return render(request,'homepage.html',context)


def task_status_new(request, task_id):
    task = AsyncResult(task_id)
    progression = 0
    if task.state == 'FAILURE' or task.state == 'PENDING':
        response = {
            'task_id': task_id,
            'state': task.state,
            'progression': progression,
            'info': str(task.info)
        }
        return JsonResponse(response, status=200)
    current = task.info.get('current', 0)
    total = task.info.get('total', 1)
    batch_no = task.info.get('batch_no', 3)

    progression = (int(current) / int(total)) * 100  # to display a percentage of progress of the task

    # if progression == 100:
    #     message = f"You have successfully uploaded the file in AIMS with batch no -> {batch_no}"
    #     messages.success(request, message)

    response = {
        'task_id': task_id,
        'state': task.state,
        'progression': progression,
        'info': "Uploading",
        'batch_no': batch_no
    }
    return JsonResponse(response, status=200)


def task_status(request, task_id):
    task = AsyncResult(task_id)
    progression = 0
    if task.state == 'FAILURE' or task.state == 'PENDING':
        response = {
            'task_id': task_id,
            'state': task.state,
            'progression': progression,
            'info': str(task.info)
        }
        return JsonResponse(response, status=200)
    current = task.info.get('current', 0)
    total = task.info.get('total', 1)
    errors = task.info.get('errors', 2)
    fin_data = task.info.get('fin_data', 3)


    progression = (int(current) / int(total)) * 100  # to display a percentage of progress of the task
    response = {
        'task_id': task_id,
        'state': task.state,
        'progression': progression,
        'info': "Validation",
        'errors': json.dumps(errors),
        'fin_data':  json.dumps(fin_data)
    }
    return JsonResponse(response, status=200)


def run_long_task(request):
    if request.method == 'POST':
        csv_file = request.FILES["file"]
        file = csv_file.read().decode('utf-8')
        csv_data = csv.reader(StringIO(file), delimiter=',')
        new_list = []
        for row in csv_data:
            new_list.append(row)
        count = 0
        new_list.pop(0)
        #print(len(new_list))
        fin_data = new_list
        task = loop.delay(fin_data)
        #print(task.id)
        return JsonResponse({"task_id": task.id}, status=202)


def progress_view(request):
    result = validate_fin_data_new.delay([10,20,30,40,50])
    print(result.task_id)

    batches = Fobatch.objects.using('finance').all()
    context = {
        'batches': batches,
        'policy_no': '100100162',
        'username': 'nicholas',
        'task_id': result.task_id
    }
    return render(request, 'display_progress.html', context)

def upload_fin(request,username):
    batches = Fobatch.objects.using('finance').all()
    context = {
        'batches': batches,
        'policy_no': '100100162',
        'username': username
    }
    return render(request,'uploadFinance.html',context)


def get_curr_record(request):
    serial = Batchcode.objects.using('finance').get(batch_type='STO')
    batch_no = 'BA' + format(serial.batch_serial, '06')
    print(f"Get batch No -- {batch_no}")
    w_curr = Bankstateovpload.objects.using('finance').filter(batch_no=batch_no).count()
    return JsonResponse({'data': w_curr,'batch_no': batch_no })


def get_number_records(request,username):
    try:
        print(f"Get number of records  -> {username}")
        print(request.FILES["file"])
        csv_file = request.FILES["file"]
        file = csv_file.read().decode('utf-8')
        csv_data = csv.reader(StringIO(file), delimiter=',')
        new_list = []
        for row in csv_data:
            new_list.append(row)
        new_list.pop(0)
        # print(new_list)
        return JsonResponse({'data': len(new_list) })

    except Exception as e:
        return JsonResponse({'data':'Something went wrong!!!'})


def upload_fin_csv_2(request,username):
    try:
        print(f"Upload premium information by -> {username}")
        print(request)
        csv_file = request.FILES["file"]
        file = csv_file.read().decode('utf-8')
        csv_data = csv.reader(StringIO(file), delimiter=',')
        new_list = []
        for row in csv_data:
            new_list.append(row)
        count = 0
        new_list.pop(0)
        print(new_list[0][0])
        fin_data = new_list
        w_count = 0
        w_prem = 0

        batch = Fobatch.objects.using('finance').create(
            batch_no=get_next_serial(),
            batch_type='REF',
            ref_no=str(new_list[0][1]).strip(),
            uploaded_by=username,
            uploaded_date=date_time,
            create_date=date_time
        )
        batch.save()
        w_policy = ''
        w_proposal = ''
        w_client_no = ''
        w_plan = ''
        w_status = ''
        for i in range(0, len(fin_data)):
            w_count += 1
            print(f"Uploading premium information record - {w_count}")
            if fin_data[i][12] == 'D':
                prop = Lapro.objects.using('olfdata').get(proposal_no=fin_data[i][14])
                w_client_no = prop.client_no
                w_plan = prop.plan
                w_status = prop.status_code
            elif fin_data[i][12] == 'P':
                pol = Lapol.objects.using('olfdata').get(policy_no=fin_data[i][13])
                w_client_no= pol.client_no
                w_plan = pol.plan
                w_status = pol.status_code
            else:
                pass


            w_amount = fin_data[i][8]
            trans_amount = w_amount.replace(',', '')
            w_prem += float(trans_amount)

            # print(trans_amount)
            trans_date = datetime.strptime(fin_data[i][7], "%d/%m/%Y")
            if len(fin_data[i][14]) == 0:
                w_proposal_no = 0
                # print(f"Not empty -  {w_proposal_no}")
            else:
                w_proposal_no = fin_data[i][14]
                # print(f"Not empty -  {w_proposal_no}")

            bnk = Bankstateovpload.objects.using('finance').create(
                item_no=int(fin_data[i][0]),
                ref_no=str(fin_data[i][1]).strip(),
                corporate_code=str(fin_data[i][2]).strip(),
                source_code=str(fin_data[i][3]).strip(),
                ovp_group=str(fin_data[i][4]).strip(),
                grp_item_no=fin_data[i][5],
                group_tariff=str(fin_data[i][6]).strip(),
                trans_date=trans_date,
                trans_amount=trans_amount,
                client_name=str(fin_data[i][9]).strip(),
                member_no=fin_data[i][10],
                payroll_no=str(fin_data[i][11]),
                receipt_for=str(fin_data[i][12]).strip(),
                policy_no=str(fin_data[i][13]).strip(),
                proposal_no=w_proposal_no,
                batch_no=batch.batch_no
            )

            corp = Corpmonth.objects.using('finance').get(ref_no=bnk.ref_no)
            bankstate = Bankstatedtl.objects.using('finance').create(
                ref_no=bnk.ref_no,
                corporate_code=bnk.corporate_code,
                group_tariff=bnk.group_tariff,
                trans_amount=bnk.trans_amount,
                dola=date_time,
                date_posted=date_time,
                account_year=corp.account_year,
                account_month=corp.account_month,
                user_str=username,
                trans_date=bnk.trans_date,
                policy_no=bnk.policy_no,
                proposal_no=bnk.proposal_no,
                payroll_no=bnk.payroll_no,
                receipt_for=bnk.receipt_for,
                client_no=w_client_no,
                plan=w_plan,
                policy_status=w_status,
                client_name=bnk.client_name,
                item_no=bnk.item_no,
                grp_item_no=bnk.grp_item_no,
                ovp_group=bnk.ovp_group,
                status_code='U',
                batch_no=bnk.batch_no,
                chk_no=1
            )

        return JsonResponse({'data': w_count })


    except Exception as e:
        return JsonResponse({'data':'something went wrong!!!'})


def upload_csv(request,username):
    print(f"Upload premium information by -> {username}")
    csv_file = request.FILES["csv_file"]
    file = csv_file.read().decode('utf-8')
    csv_data = csv.reader(StringIO(file), delimiter=',')
    new_list = []
    for row in csv_data:
        new_list.append(row)
    count = 0
    new_list.pop(0)

    result = validate_fin_data_new.delay(new_list)

    batches = Fobatch.objects.using('finance').all()

    context = {
        'batches': batches,
        'policy_no': '100100162',
        'username': 'nndehi',
        'task_id': result.task_id
    }
    return render(request, 'uploadFinance.html',context)


def upload_fin_csv(request,username):

    try:
        print(f"Upload premium information by -> {username}")
        csv_file = request.FILES["csv_file"]
        file = csv_file.read().decode('utf-8')
        csv_data = csv.reader(StringIO(file), delimiter=',')
        new_list = []
        for row in csv_data:
            new_list.append(row)
        count = 0
        new_list.pop(0)
        print(new_list[0][0])

        #errors = validate_fin_data(new_list)

        errors = validate_fin_data_new(new_list[0])

        #errors = []
        if len(errors) == 0:
            batch = Fobatch.objects.using('finance').create(
                batch_no=get_next_serial(),
                batch_type='REF',
                ref_no=str(new_list[0][1]).strip(),
                uploaded_by=username,
                uploaded_date=date_time,
                create_date=date_time
            )
            batch.save()

            totals = upload_fin_data(new_list,batch)
            updateBatch = Fobatch.objects.using('finance').get(batch_no=batch.batch_no)
            updateBatch.no_of_recs = totals[0]
            updateBatch.total_premium = totals[1]
            updateBatch.save()
            print("No errors in the file !!!!")
            messages.success(request, 'You have successfully uploaded Premium details in the AIMS staging area')
        else:
            for error in errors:
                messages.error(request, error)


    except Exception as e:
        messages.error(request,e)


    batches = Fobatch.objects.using('finance').all()

    context = {
        'batches': batches,
        'policy_no': '100100162',
        'username': 'nndehi',
       }
    return render(request,'uploadFinance.html',context)


def upload_fin_data(fin_data,batch):
    w_count = 0
    w_prem = 0
    w_client_no = ''
    w_plan = ''
    w_status = ''
    for i in range(0, len(fin_data)):
        w_count += 1
        print(f"Uploading premium information record - {w_count}")
        if fin_data[i][12] == 'D':
            prop = Lapro.objects.using('olfdata').get(proposal_no__contains=str(fin_data[i][14]).strip())
            w_client_no = prop.client_no
            w_plan = prop.plan
            w_status = prop.status_code
        elif fin_data[i][12] == 'P' and fin_data[i][3] == 'OLF':
            pol = Lapol.objects.using('olfdata').get(policy_no__contains=str(fin_data[i][13]).strip())
            w_client_no = pol.client_no
            w_plan = pol.plan
            w_status = pol.status_code
        else:
            pass
        w_amount = fin_data[i][8]
        trans_amount = w_amount.replace(',','')
        w_prem += float(trans_amount)

        # print(trans_amount)
        trans_date = datetime.strptime(fin_data[i][7], "%d/%m/%Y")
        if len(fin_data[i][14]) == 0 :
            w_proposal_no = 0
            #print(f"Not empty -  {w_proposal_no}")
        else:
            w_proposal_no = fin_data[i][14]
            #print(f"Not empty -  {w_proposal_no}")
        w_member_no = 0
        if len(fin_data[i][10]) == 0:
            w_member_no = 0
        else:
            w_member_no = int( fin_data[i][10])


        bnk = Bankstateovpload.objects.using('finance').create(
            item_no=int(fin_data[i][0]),
            ref_no=str(fin_data[i][1]).strip(),
            corporate_code=str(fin_data[i][2]).strip(),
            source_code=str(fin_data[i][3]).strip(),
            ovp_group=str(fin_data[i][4]).strip(),
            grp_item_no= fin_data[i][5],
            group_tariff=str(fin_data[i][6]).strip(),
            trans_date=trans_date,
            trans_amount= trans_amount,
            client_name=str(fin_data[i][9]).strip(),
            member_no=w_member_no,
            payroll_no=str(fin_data[i][11]),
            receipt_for=str(fin_data[i][12]).strip(),
            policy_no=str(fin_data[i][13]).strip(),
            proposal_no=w_proposal_no,
            batch_no=batch.batch_no
        )
        corp = Corpmonth.objects.using('finance').get(ref_no=bnk.ref_no)

        bankstate = Bankstatedtl.objects.using('finance').create(
            ref_no=bnk.ref_no,
            corporate_code=bnk.corporate_code,
            group_tariff=bnk.group_tariff,
            trans_amount=bnk.trans_amount,
            dola=date_time,
            date_posted=date_time,
            account_year=corp.account_year,
            account_month=corp.account_month,
            user_str=batch.uploaded_by,
            trans_date=bnk.trans_date,
            policy_no=bnk.policy_no,
            proposal_no=bnk.proposal_no,
            payroll_no=bnk.payroll_no,
            receipt_for=bnk.receipt_for,
            client_no=w_client_no,
            plan=w_plan,
            policy_status=w_status,
            client_name=bnk.client_name,
            item_no=bnk.item_no,
            grp_item_no=bnk.grp_item_no,
            ovp_group=bnk.ovp_group,
            status_code='U',
            batch_no=bnk.batch_no,
            chk_no=1,
            source_code=bnk.source_code
        )

    return [w_count,w_prem]


def validate_fin_data(fin_data):
    errors = []
    count = 0

    policy_list = []
    proposal_list = []

    for i in range(0, len(fin_data)):
        count += 1
        print(fin_data[i])
        if fin_data[i][12] == 'D' :
            proposal_list.append(fin_data[i][14])
        if fin_data[i][12] == 'P':
            policy_list.append(fin_data[i][13])

        if Corpmonth.objects.using('finance').filter(ref_no=str(fin_data[i][1]).strip()).count() == 0:
            errors.append(f"The statement reference does not exist in AIMS at line no -> {count}")

        if fin_data[i][12] not in ['P','D','S']:
            errors.append(f"Receipt for should either be D[Deposit] / P[Policy] / S[Suspense] at line {count}")
            
        if len(fin_data[i][13]) == 0 and fin_data[i][12] == 'P':
            errors.append(f"Please capture the policy no at line no  -> {count}")
            
        if len(fin_data[i][14]) == 0 and fin_data[i][12] == 'D':
            errors.append(f"Please capture the proposal no at line no  ->{fin_data[i][14]} -- {count}")
            
        if Lapol.objects.using('olfdata').filter(policy_no__contains=str(fin_data[i][13]).strip()).count() == 0 and  fin_data[i][12] == 'P' and fin_data[i][3] == 'OLF':
            errors.append(f"The policy no does not exist in AIMS at line no -> {count}")
            
        if Lapro.objects.using('olfdata').filter(proposal_no__contains=str(fin_data[i][14]).strip()).count() == 0 and  fin_data[i][12] == 'D' and fin_data[i][3] == 'OLF':
            errors.append(f"The proposal no does not exist in AIMS at line no -> {count}")
        if Lapol.objects.using('olfdata').filter(proposal_no__contains=fin_data[i][14]).count() > 0 and fin_data[i][12] == 'D':
            errors.append(f"The proposal has already been converted to a policy at line -> {count}")

    dup_pol = repeat(policy_list)
    dup_prop = repeat(proposal_list)

    print(dup_pol)
    if len(dup_pol) > 0 and fin_data[i][3] == 'OLF':
        for pol in dup_pol:
            errors.append(f"The policy no has already been used  -> {pol} ")

    print(dup_prop)
    if len(dup_prop) > 0:
        for prop in dup_prop:
            errors.append(f"The proposal no has already been used   -> {prop} ")

    return errors


def repeat(x):
    _size = len(x)
    repeated = []
    for i in range(_size):
        k = i + 1
        for j in range(k, _size):
            if x[i] == x[j] and x[i] not in repeated:
                repeated.append(x[i])
    return repeated


def get_next_serial():
    serial = Batchcode.objects.using('finance').get(batch_type='STO')
    batch_no = 'BA' + format(serial.batch_serial, '06')
    serial.batch_serial = serial.batch_serial + 1
    serial.save()
    return batch_no
