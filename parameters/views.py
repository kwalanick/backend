from django.shortcuts import render,get_object_or_404
from django.contrib import messages,auth
from uploads.models import Glrates,Premrates,Glrdrate,BatchCode,Fleetusers
from datetime import datetime,date
from io import StringIO
import re
import csv
import datetime


# Create your views here.
def upload_form(request,username):

    return render(request,'uploadPremRates.html')

def upload_csv(request,username):
    return render(request,'uploadPremRates.html')


# def batch_detail(request,batch_no,username):
#
#     clients = ClientUpload.objects.filter(batch_no=batch_no)
#     context = {
#         "batch_no" : batch_no,
#         "clients" : clients,
#         "username" : username
#     }
#     return render(request,'client_details.html',context)

def process_batch(request,username):
    return render(request,'uploadPremRates.html')

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
    return render(request,'uploadPremRates.html',context)

