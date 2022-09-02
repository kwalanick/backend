from django.urls import path ,include
from . import views


urlpatterns = [

    path('upload_form/<str:username>/',views.upload_form,name='param_upload_form'),
    path('upload_csv/<str:username>/',views.upload_csv,name='param_upload_csv'),
    path('batch/<str:username>/',views.upload_csv,name='param_upload_csv'),
    path('review/<str:username>/',views.review_upload,name='param_review_upload'),
    path('process_batch/<str:batch_no>/<str:username>/',views.process_batch,name='client_process'),

]
