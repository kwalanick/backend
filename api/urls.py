from django.urls import path,include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    #TokenRefreshView,
)
from . import views

router = routers.DefaultRouter()
#router.register('members',views.MemberViewSet)
router.register('membersupload',views.MemberUploadViewSet)




urlpatterns = [
    path('users/login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('',views.getRoutes,name ='get-routes'),
    #path('',include(router.urls),),

    path('clients/',views.client_list,name ='clients'),
    path('clients/client_no/<str:client_no>/',views.client_detail,name ='get_client'),
    path('clients/<str:id_number>/',views.get_client_id,name ='get_client_id'),
    path('clients/update/<str:client_no>/',views.update_client,name ='update_client'),

    path('schemes/',views.get_schemes,name ='schemes'),
    path('schemes/<str:policy_no>/',views.scheme_detail,name ='scheme_detail'),

    path('members/',views.get_members,name ='members'),
    path('members/<str:policy_no>/<str:member_no>/',views.member_detail,name ='member_detail'),
    path('members/create/',views.create_member,name ='create_member'),
    path('members/update/<str:policy_no>/<str:member_no>/',views.update_member,name ='update_member'),


    path('loans/',views.get_loans,name ='loans'),
    path('loans/<str:policy_no>/<str:member_no>/<str:loan_no>/',views.get_loan_detail,name ='loans'),
    path('loans/create/',views.create_loan,name ='create_loan'),
    path('loans/update/<str:policy_no>/<str:member_no>/<str:loan_no>/',views.update_loan,name ='update_loan'),

    path('jointmembers/', views.get_joint_members, name='joint_members'),
    path('jointmembers/create/', views.create_joint_member, name='create_joint'),
    path('jointmembers/<str:client_no>/', views.get_joint_member, name='joint_member'),


    path('riders_params/',views.get_ridersparams,name ='rider_params'),
    path('riders/',views.get_riders,name ='riders'),
    path('riders/create/',views.create_rider,name ='create_rider'),
    path('riders/update_life/<str:policy_no>/<str:member_no>/<str:uw_year>/rider_code/',
         views.update_rider_life,name ='update_rider_life'),
    path('riders/update_credit/<str:policy_no>/<str:member_no>/<str:loan_no>/<str:uw_year>/rider_code/',
         views.update_rider_credit,name ='update_rider_credit'),


    path('healthrecords/',views.get_health_records,name ='health_records'),
    path('healthrecords/create/',views.create_health_record,name ='create_health_record'),
    path('healthrecords/update/<str:policy_no>/<str:member_no>/<str:loan_no>/',views.update_health_record,name='update_health_record'),

    path('countries/',views.get_countries,name ='countries'),


    path('provinces/',views.get_provinces,name ='provinces'),
    path('districts/',views.get_districts,name ='districts'),
    path('sectors/',views.get_sectors,name ='sectors'),
    path('cells/',views.get_cells,name ='cells'),
    path('villages/',views.get_villages,name ='villages'),

    path('identities/',views.get_identities,name ='identities'),
    path('titles/',views.get_titles,name ='titles'),
    path('bnrcodes/',views.get_bnrcodes,name ='bnrcodes'),
    path('maritalstatus/',views.get_maritals,name ='maritalstatus'),
    path('industries/',views.get_industries,name ='industries'),
    path('economic_subs/',views.get_economic_subs,name ='economic_subs'),
    path('relations/',views.get_relations,name ='relations'),
    path('status/',views.get_statuses,name ='statuses'),
    path('occupations/',views.get_occupations,name ='occupations'),

]
