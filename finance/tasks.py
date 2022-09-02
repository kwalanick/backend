from __future__ import absolute_import,unicode_literals

from celery import shared_task
from celery_progress.backend import ProgressRecorder
import time
from backend.celery import app
from .models import Lapol,Lapro,Corpmonth,Fobatch,Batchcode,Bankstatedtl,Bankstateovpload,Corpmonthschedgrp,Corpmonthsusp
from .views import date_time
from datetime import datetime, date


@shared_task
def add(x,y):
    return x+y



@app.task(bind=True)
def update_bankstate(self,fin_data,username):
    errors = []
    print(fin_data)
    batch = Fobatch.objects.using('finance').create(
        batch_no=get_next_serial(),
        batch_type='REF',
        ref_no=fin_data[0][1],
        uploaded_by=username,
        uploaded_date=date_time,
        create_date=date_time
    )
    batch.save()

    totals = upload_fin_data(self,fin_data, batch)
    updateBatch = Fobatch.objects.using('finance').get(batch_no=batch.batch_no)
    updateBatch.no_of_recs = totals[0]
    updateBatch.total_premium = totals[1]
    updateBatch.save()

    return {'current': 100, 'total': 100,'batch_no': batch.batch_no }


@app.task(bind=True)
def loop(self, fin_data):
    errors = []
    count = 0

    policy_list = []
    proposal_list = []
    for i in range(int(len(fin_data))):
        # print(i)
        # time.sleep(1)
        count += 1
        if fin_data[i][12] == 'D':
            proposal_list.append(fin_data[i][14])
        if fin_data[i][12] == 'P':
            policy_list.append(fin_data[i][13])

        # str(fin_data[i][9])
        if len(str(fin_data[i][9])) > 100 :
            errors.append(f"Maximum length for client name is 100  -> {count}")

        if Corpmonth.objects.using('finance').filter(ref_no=str(fin_data[i][1]).strip()).count() == 0:
            errors.append(f"The statement reference does not exist in AIMS at line no -> {count}")

        if fin_data[i][12] not in ['P', 'D', 'S'] and fin_data[i][3] == 'OLF':
            errors.append(f"Receipt for should either be D[Deposit] / P[Policy] / S[Suspense] at line {count}")

        if len(fin_data[i][13]) == 0 and fin_data[i][12] == 'P':
            errors.append(f"Please capture the policy no at line no  -> {count}")

        if len(fin_data[i][14]) == 0 and fin_data[i][12] == 'D':
            errors.append(f"Please capture the proposal no at line no  ->{fin_data[i][14]} -- {count}")

        if Lapol.objects.using('olfdata').filter(policy_no__contains=str(fin_data[i][13]).strip()).count() == 0 and \
                fin_data[i][12] == 'P' and fin_data[i][3] == 'OLF':
            errors.append(f"The policy no does not exist in AIMS at line no -> {count}")

        if Lapro.objects.using('olfdata').filter(proposal_no__contains=str(fin_data[i][14]).strip()).count() == 0 and \
                fin_data[i][12] == 'D' and fin_data[i][3] == 'OLF':
            errors.append(f"The proposal no does not exist in AIMS at line no -> {count}")

        if Lapro.objects.using('olfdata').filter(proposal_no__contains=str(fin_data[i][14]).strip()).count() > 0 and \
                fin_data[i][12] == 'D' and fin_data[i][3] == 'OLF':
            if Lapro.objects.using('olfdata').get(proposal_no__contains=str(fin_data[i][14]).strip()).status_code !='01':
                errors.append(f"The proposal status not pre-issued -> {count}")

        if Lapol.objects.using('olfdata').filter(proposal_no__contains=fin_data[i][14]).count() > 0 and fin_data[i][
            12] == 'D':
            errors.append(f"The proposal has already been converted to a policy at line -> {count}")
        self.update_state(state='PROGRESS',meta={'current': i, 'total': len(fin_data)})

    print('Task completed')
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
    print(fin_data[0][1])
    #if Fobatch.objects.using('finance').filter(ref_no__contains=str(fin_data[0][1]).strip()).count() > 0:
    #    errors.append(f"Batch with existing reference exists !!!! ")
    #print(errors)
    return {'current': 100, 'total': 100, 'errors': errors , 'fin_data': fin_data }


@shared_task(bind=True)
def my_task(self, seconds):
    progress_recorder = ProgressRecorder(self)
    result = 0
    for i in range(seconds):
        time.sleep(1)
        result += i
        progress_recorder.set_progress(i + 1, seconds)
    return result



@shared_task(bind=True)
def validate_fin_data_new(self,fin_data):
    progress_recorder = ProgressRecorder(self)
    result = 0

    for i in range(len(fin_data)):
        #time.sleep(0.1)
        result += i
        progress_recorder.set_progress(i + 1, len(fin_data))

    return result


def upload_fin_data(this,fin_data,batch):
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
            client_name=str(bnk.client_name),
            item_no=bnk.item_no,
            grp_item_no=bnk.grp_item_no,
            ovp_group=bnk.ovp_group,
            status_code='U',
            batch_no=bnk.batch_no,
            chk_no=1,
            source_code=bnk.source_code
        )

        this.update_state(state='PROGRESS', meta={'current': i, 'total': len(fin_data)})

    if Corpmonthschedgrp.objects.using('finance').filter(ref_no__contains=str(fin_data[i][1]).strip()).count() > 0:
        update_prem = Corpmonthschedgrp.objects.using('finance').filter(ref_no__contains=str(fin_data[i][1]).strip()).update(
            batch_no=batch.batch_no
        )
    if Corpmonthsusp.objects.using('finance').filter(ref_no__contains=str(fin_data[i][1]).strip()).count() > 0:
        update_susp = Corpmonthsusp.objects.using('finance').filter(ref_no__contains=str(fin_data[i][1]).strip()).update(
            batch_no = batch.batch_no
        )

    return [w_count,w_prem]


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