from django.urls import path,include
from . import views


urlpatterns = [

    path('',views.test_project,name='home'),
    path('upload_form/<str:user_id>/',views.upload_form,name='upload_form'),
    path('upload_csv/<str:username>/',views.upload_csv,name='upload_csv'),
    path('batch/<str:batch_no>/<str:username>/',views.batch_detail,name='batch_detail'),
    path('review/<str:batch_no>/<str:policy_no>/<str:username>',views.review_upload , name='review_upload'),
    path('process_batch/<str:batch_no>/<str:policy_no>/<str:username>/',views.process_batch,name='process_batch')

]

