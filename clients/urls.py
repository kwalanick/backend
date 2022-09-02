from django.urls import path,include
from . import views

urlpatterns = [
    path('upload_form/<str:username>/',views.upload_form,name='client_form'),
    path('upload_csv/<str:username>/',views.upload_csv,name='client_csv'),
    path('batch/<str:batch_no>/<str:username>/',views.batch_detail,name='batch_detail'),
    path('review/<str:batch_no>/<str:username>/',views.review_upload,name='client_review'),
    path('process_batch/<str:batch_no>/<str:username>/',views.process_batch,name='client_process'),
]