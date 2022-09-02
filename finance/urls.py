from django.urls import path , include
from . import views


urlpatterns = [
    path('upload_fin/<str:username>',views.upload_fin,name='upload_fin'),
    path('get_number_records/<str:username>/',views.get_number_records,name='get_number_records'),
    path('get_curr_record/',views.get_curr_record,name='get_curr_record'),
    path('upload_fin_csv/<str:username>/',views.upload_csv,name='upload_csv'),
    path('progress/',views.progress_view,name='progress_view'),
    path('home/<str:username>/',views.home,name='home'),
    path('run-long-task/', views.run_long_task, name='run_long_task'),
    path('upload_data/', views.upload_data, name='upload_data'),
    path('task-status/<str:task_id>/', views.task_status, name='task_status'),
    path('task-status-new/<str:task_id>/',views.task_status_new, name='task_status_new'),
]