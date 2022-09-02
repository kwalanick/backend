from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status

from .serializers import UserSerializerWithToken, ClientSerializer, MembermasterSerializer, \
    MemberUploadSerializer, SchemeSerializer, ProvinceSerializer, DistrictSerializer, SectorsSerializer, \
    CellsSerializer, VillagesSerializer, IdentitySerializer, BnrSerializer, MaritalSerializer, \
    IndustrySerializer, EconomicSerializer, RelationSerializer, StatusSerializer, LoanSerializer, \
    HealthSerializer, RiderSerializer, CountrySerializer, OccupationSerializer, RidersParamSerializer, \
    TitleSerializer,JointMemberSerializer

from rest_framework.pagination import PageNumberPagination

# models

from uploads.models import Glclmast, Membermaster, MemberupdNew, Schememaster, Glmploan, Glcrhealthq, Glmmridtl, \
    Glriders,Gljointmst
from clients.models import Provinces, Districts, Sectors, Cells, Village, Countryparam, Glidentity, \
    Bnrclassification, Glmasta, NaicsCodes, Glrelation, Glstatus, EconomicSubSectors, Occupation, Gltitle
from uploads.views import gen_client_num
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
date_time = date.today()

from .errors.validate_client import validate_client_req
from .errors.validate_member import validate_member
from .errors.validate_loans import validate_loan_errors
from .errors.validate_rider_errors import validate_riders
from .errors.validate_health_info import validate_health_records
from .errors.validate_joint import validate_joint_member



# Create your views here.
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



@api_view(['GET'])
def getClients(request):
    clients = Glclmast.objects.all()
    serializer = ClientSerializer(clients, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getMembers(request):
    members = Membermaster.objects.filter(policy_no='700100269')
    serializer = MembermasterSerializer(members, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/clients/',
        '/api/clients/<id>',
        '/api/clients/update/<id>'
    ]
    return Response(routes)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_schemes(request):
    schemes = Schememaster.objects.all()
    try:
        serializer = SchemeSerializer(schemes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(e, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def scheme_detail(request, policy_no):
    try:
        scheme = Schememaster.objects.get(policy_no=policy_no)
        serializer = SchemeSerializer(scheme, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(e, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_members(request):
    try:
        members = Membermaster.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 100
        result_page = paginator.paginate_queryset(members, request)
        serializer = MembermasterSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    except Exception as e:
        return Response(e, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def member_detail(request, policy_no, member_no):
    try:
        member = Membermaster.objects.get(policy_no=policy_no, member_no=member_no)
        serializer = MembermasterSerializer(member, many=False)
        #print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        message = {'Error': 'The member does not exist in the scheme '}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'PUT'])
@permission_classes([IsAuthenticated])
def create_member(request):
    if request.method == 'POST':
        print(request.data)
        member_no = 0
        try:
            data = request.data
            errors = validate_member(request, data)

            if len(errors) == 0:
                
                members =  Membermaster.objects.filter(policy_no=data['policy_no'])
                member_serials = [num.member_no for num in members]
                if len(member_serials) == 0:
                    member_no = 1
                else:
                    member_no = max(member_serials) + 1
                #member_no = Membermaster.objects.filter(policy_no=data['policy_no']).count() + 1
                join_date_1 = datetime.strptime(data['join_date'], "%d/%m/%Y")
                employment_date_1 = datetime.strptime(data['employment_date'], "%d/%m/%Y")
                uw_date = datetime.strptime(data['uw_date'], "%d/%m/%Y")
                created_date = datetime.strptime(data['created_date'], "%d/%m/%Y")
                # date_left = datetime.strptime(data['date_left'], "%d/%m/%Y")
                dob = datetime.strptime(data['dob'], "%d/%m/%Y")
                modified_date = datetime.strptime(data['modified_date'], "%d/%m/%Y")
                period_from = datetime.strptime(data['period_from'], "%d/%m/%Y")
                period_to = datetime.strptime(data['period_to'], "%d/%m/%Y")
                maturity_date = datetime.strptime(data['maturity_date'], "%d/%m/%Y")
                scheme = Schememaster.objects.get(policy_no=data['policy_no'])
                
                if Membermaster.objects.filter(policy_no=data['policy_no'],client_no=data['client_no']).count() == 0:
                    member = Membermaster.objects.create(
                        policy_no=data['policy_no'],
                        client_no=data['client_no'],
                        member_no=member_no,
                        uw_year=data['uw_year'],
                        status_code=1,
                        institute_client_number=data['institute_client_number'],
                        payroll_no=data['payroll_no'],
                        surname=data['surname'],
                        first_name=data['first_name'],
                        other_names=data['other_names'],
                        name=data['surname'] + ' ' + data['first_name'],
                        gender=data['gender'],
                        join_date=join_date_1,
                        employment_date=employment_date_1,
                        uw_date=uw_date,
                        created_date=created_date,
                        # date_left=date_left,
                        dob=dob,
                        age=data['age'],
                        modified_date=modified_date,
                        modified_by=data['modified_by'],
                        period_from=period_from,
                        period_to=period_to,
                        term_years=data['term_years'],
                        pay_freq=data['pay_freq'],
                        current_salary=data['monthly_salary'],
                        annual_salary=data['annual_salary'],
                        maturity_date=maturity_date,
                        date_created=created_date,
                        branch=data['branch'],
                        agent=data['agent'],
                        retirement_age=data['retirement_age'],
                        lc_cover_factor=1,  # scheme.lc_factor,
                        total_sum_assured=data['total_sum_assured'],
                        orig_sum_insured=data['total_sum_assured'],
                        restricted_sum_assured=data['total_sum_assured'],
                        est_loan_amount=data['est_loan_amount'],
                        rider_benefit=data['rider_benefit'],
                        rider_premium=data['rider_premium'],
                        lc_norm_annual_prem=data['premium'],
                        lc_new_annual_prem=data['premium'],
                        lc_total_annual_prem=data['total_premium'],
                        crm_flag='Y'
                    )
                    message = {
                        'success': f'You have successful created a new member in  {scheme.scheme_name} ',
                        'member_no': member_no,
                    }
                    return Response(message, status=status.HTTP_201_CREATED)
                else:
                    member = Membermaster.objects.get(policy_no=data['policy_no'],client_no=data['client_no'])
                    message = {
                        'detail': f'Client already exist in the scheme',
                        'member_no' : member.member_no
                    }
                    return Response(message,status=status.HTTP_200_OK)
                
            else:
                member_errors = []
                count = 1
                for error in errors:
                    member_errors.append({count: error})
                    count += 1
                return Response(member_errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
    else:
        pass




@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_member(request, policy_no, member_no):
    try:
        data = request.data
        errors = validate_member(request, data)

        if len(errors) == 0:
            join_date_1 = datetime.strptime(data['join_date'], "%d/%m/%Y")
            employment_date_1 = datetime.strptime(data['employment_date'], "%d/%m/%Y")
            uw_date = datetime.strptime(data['uw_date'], "%d/%m/%Y")
            created_date = datetime.strptime(data['created_date'], "%d/%m/%Y")
            dob = datetime.strptime(data['dob'], "%d/%m/%Y")
            modified_date = datetime.strptime(data['modified_date'], "%d/%m/%Y")
            period_from = datetime.strptime(data['period_from'], "%d/%m/%Y")
            period_to = datetime.strptime(data['period_to'], "%d/%m/%Y")
            maturity_date = datetime.strptime(data['maturity_date'], "%d/%m/%Y")
            scheme = Schememaster.objects.get(policy_no=policy_no)

            # member_count = Membermaster.objects.filter(policy_no=policy_no,member_no=member_no).count()
            # print(f"Member count in update  "+member_count)

            if Membermaster.objects.filter(policy_no=policy_no, member_no=member_no).count() > 0:
                member = Membermaster.objects.filter(policy_no=policy_no, member_no=member_no).update(
                    # policy_no=policy_no,
                    # client_no=data['client_no'],
                    # member_no=member_no,
                    uw_year=data['uw_year'],
                    status_code=1,
                    institute_client_number=data['institute_client_number'],
                    payroll_no=data['payroll_no'],
                    surname=data['surname'],
                    first_name=data['first_name'],
                    other_names=data['other_names'],
                    name=data['surname'] + ' ' + data['first_name'],
                    gender=data['gender'],
                    join_date=join_date_1,
                    employment_date=employment_date_1,
                    uw_date=uw_date,
                    created_date=created_date,
                    # date_left=date_left,
                    dob=dob,
                    age=data['age'],
                    modified_date=modified_date,
                    modified_by=data['modified_by'],
                    period_from=period_from,
                    period_to=period_to,
                    term_years=data['term_years'],
                    pay_freq=data['pay_freq'],
                    current_salary=data['monthly_salary'],
                    annual_salary=data['annual_salary'],
                    maturity_date=maturity_date,
                    date_created=created_date,
                    branch=data['branch'],
                    agent=data['agent'],
                    retirement_age=data['retirement_age'],
                    lc_cover_factor=1,  # scheme.lc_factor,
                    total_sum_assured=data['total_sum_assured'],
                    orig_sum_insured=data['total_sum_assured'],
                    restricted_sum_assured=data['total_sum_assured'],
                    est_loan_amount=data['est_loan_amount'],
                    rider_benefit=data['rider_benefit'],
                    rider_premium=data['rider_premium'],
                    lc_norm_annual_prem=data['premium'],
                    lc_new_annual_prem=data['premium'],
                    lc_total_annual_prem=data['total_premium']
                )
                message = {
                    'success': f'You have successful updated a new member in  {scheme.scheme_name} ',
                    'member_no': member_no,
                }
                return Response(message, status=status.HTTP_200_OK)
            else:
                message = {'error': 'The member does not exist in the scheme '}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            member_errors = []
            count = 1
            for error in errors:
                member_errors.append({count: error})
                count += 1
            return Response(member_errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response(e, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_client_id(request, id_number):
    try:
        client = Glclmast.objects.get(identity_card_no__contains=id_number)
        serializer = ClientSerializer(client, many=False)
        message = {
            'success': 'OK',
            'client_no': client.client_no
        }
        return Response(message, status=status.HTTP_200_OK)
    except Exception as e:
        message = {'Detail': 'The client ID does not exist in AIMS'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def client_list(request):
    if request.method == 'GET':
        clients = Glclmast.objects.all()

        paginator = PageNumberPagination()
        paginator.page_size = 100
        result_page = paginator.paginate_queryset(clients, request)
        serializer = ClientSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    elif request.method == 'POST':
        data = request.data
        #print(data)
        try:
            print(data)
            errors = validate_client_req(data)
            if len(errors) == 0:
                bnr_classification = (data['bnr_classification']).strip()
                title = data['title']
                surname = (data['surname']).upper().strip()
                other_names = (data['other_names']).upper().strip()
                resident_country = data['resident_country']  # check
                country_code = data['country_code']  # check
                identity_card_no = data['identity_card_no']  # check
                id_doc = int(data['id_doc'])
                gender = data['gender']
                marital_status = str(data['marital_status'])  # check
                spourse_name = (data['spourse_name']).upper().strip()
                birth_date_1 = data['birth_date']  # check
                birth_date = datetime.strptime(birth_date_1, "%d/%m/%Y")  # check
                birth_reg_village = data['birth_reg_village']  # check
                residence_type = data['residence_type']  # check O / T
                email = data['email']  # validate email address
                mobile_no = data['mobile_no']  # validate mobile
                telephone = data['telephone']
                fax = data['fax']
                occupation = data['occupation']  # check from AIMS
                naics_code = data['naics_code']  # check from AIMS
                economic_sub_sector = data['economic_sub_sector']  # check from AIMS
                relation_to_company_code = data['relation_to_company_code']  # check from AIMS
                province = data['province']  # check from AIMS
                district = data['district']  # check from AIMS
                sector = data['sector']  # check from AIMS
                cellule = data['cellule']  # check from AIMS
                village = data['village']  # check from AIMS
                contact = data['contact']  # check from AIMS
                contact_position = data['contact_position']
                contact_telephone = data['contact_telephone']  # check from AIMS
                address = data['address']
                address2 = data['address2']
                address3 = data['address3']

                print(data['contact_telephone'])
                # get client number
                client_number = gen_client_num(surname)
                full_names = surname + ' ' + other_names
                client_type = 'I' if bnr_classification == '001' else 'C'
                id_unique = identity_card_no[0:13]  # if (data['id_doc'] == 2) else identity_card_no.strip()

                print(f"Generated client number  - {client_number} - {identity_card_no}")
                try:
                    if Glclmast.objects.filter(id_unique__contains=id_unique).count() == 0:
                        print("Adding .................")
                        print(data)
                        new_client = Glclmast.objects.create(
                            client_no=client_number,
                            bnr_classification=bnr_classification,
                            surname=surname,
                            other_names=other_names,
                            client_type=client_type,
                            name=str(full_names).ljust(200,' '),
                            resident_country=resident_country,
                            country_code=country_code,
                            identity_card_no=identity_card_no,
                            id_unique=id_unique,
                            id_doc=id_doc,
                            gender=gender,
                            marital_status=marital_status,
                            spourse_name=spourse_name,
                            birth_date=birth_date,
                            birth_reg_village=birth_reg_village,
                            residence_type=residence_type,
                            address=address,
                            address2=address2,
                            address3=address3,
                            email=email,
                            mobile_no=mobile_no,
                            telephone=telephone,
                            fax=fax,
                            occupation=occupation,
                            naics_code=naics_code,
                            economic_sub_sector=economic_sub_sector,
                            relation_to_company_code=relation_to_company_code,
                            province=province,
                            district=district,
                            sector=sector,
                            cellule=cellule,
                            village=village,
                            contact=contact,
                            contact_position=contact_position,
                            contact_telephone=contact_telephone,
                            crm_flag_new='Y',
                            title=data['title'],
                            creation_date=date_time
                        )
                        print("Test 1")
                        message = {
                            'success': f"You have successfully created a new client in AIMS",
                            'client_no': client_number
                        }
                        return Response(message, status=status.HTTP_201_CREATED)
                    else:
                        print("Editing.................")
                        print(data)
                        client_instance = Glclmast.objects.get(id_unique__contains=id_unique.strip())
                        message = {
                            'success': f"The client already exists in AIMS ",
                            'client_no': client_instance.client_no
                        }
                        return Response(message, status=status.HTTP_200_OK)
                except Exception as e:
                    message = {'Detail': 'Error while creating a client'}
                    return Response(e, status=status.HTTP_400_BAD_REQUEST)

            else:
                client_errors = []
                count = 1

                for error in errors:
                    client_errors.append({count: error})
                    count += 1
                return Response(client_errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            message = {'error': 'Client creation failed 1. Errors in request data posted check for empty fields'}
            return Response(e, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def client_detail(request, client_no):
    print(client_no)
    try:
        client = Glclmast.objects.get(client_no=client_no)
        serializer = ClientSerializer(client, many=False)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        message = {'Detail': 'The client  does not exist in AIMS'}
        return Response(message, status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_client(request, client_no):
    data = request.data
    errors = validate_client_req(data)

    if len(errors) == 0:
        print(f"Check where we are - {client_no}")
        client_type = 'I' if data['bnr_classification'] == '001' else 'C'
        if Glclmast.objects.filter(client_no=client_no).count() > 0:

            client = Glclmast.objects.get(client_no=client_no)

            if client.identity_card_no[0:13] != data['identity_card_no'][0:13] and data['id_doc'] == 2:
                message = 'The first 13 characters in an ID cannot be changed'
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            else:
                try:
                    update_client = Glclmast.objects.filter(client_no__contains=client_no).update(
                        title=data['title'] if len(data['title']) != 0 else client.title,
                        surname=(data['surname']).upper() if len(data['surname']) != 0 else client.surname,
                        other_names=(data['other_names']).upper() if len(
                            data['other_names']) != 0 else client.other_names,
                        resident_country=data['resident_country'] if len(
                            data['resident_country']) != 0 else client.resident_country,
                        country_code=data['country_code'] if len(data['country_code']) != 0 else client.country_code,
                        identity_card_no=data['identity_card_no'] if len(
                            data['identity_card_no']) != 0 else client.identity_card_no,
                        gender=data['gender'] if len(data['gender']) != 0 else client.gender,
                        marital_status=data['marital_status'] if len(
                            data['marital_status']) != 0 else client.marital_status,
                        spourse_name=data['spourse_name'] if len(data['spourse_name']) != 0 else client.spourse_name,
                        birth_date=datetime.strptime(data['birth_date'], "%d/%m/%Y") if len(
                            data['birth_date']) != 0 else client.birth_date,  # check
                        birth_reg_village=data['birth_reg_village'] if len(
                            data['birth_reg_village']) != 0 else client.birth_reg_village,
                        residence_type=data['residence_type'] if len(
                            data['residence_type']) != 0 else client.residence_type,
                        email=data['email'] if len(data['email']) != 0 else client.email,
                        mobile_no=data['mobile_no'] if len(data['mobile_no']) != 0 else client.mobile_no,
                        telephone=data['telephone'] if len(data['telephone']) != 0 else client.telephone,
                        fax=data['fax'] if len(data['fax']) != 0 else client.fax,
                        occupation=data['occupation'] if len(data['occupation']) != 0 else client.occupation,
                        naics_code=data['naics_code'] if len(data['naics_code']) != 0 else client.naics_code,
                        economic_sub_sector=data['economic_sub_sector'] if len(
                            data['economic_sub_sector']) != 0 else client.economic_sub_sector,
                        relation_to_company_code=data['relation_to_company_code'] if len(
                            data['relation_to_company_code']) != 0 else client.relation_to_company_code,
                        province=data['province'] if len(data['province']) != 0 else client.province,
                        district=data['district'] if len(data['district']) != 0 else client.district,
                        sector=data['sector'] if len(data['sector']) != 0 else client.sector,
                        cellule=data['cellule'] if len(data['cellule']) != 0 else client.cellule,
                        village=data['village'] if len(data['village']) != 0 else client.village,
                        contact=data['contact'] if len(data['contact']) != 0 else client.contact,
                        contact_position=data['contact_position'] if len(
                            data['contact_position']) != 0 else client.contact_position,
                        contact_telephone=data['contact_telephone'] if len(
                            data['contact_telephone']) != 0 else client.contact_telephone,
                        address=data['address'] if len(data['address']) != 0 else client.address,
                        address2=data['address2'] if len(data['address2']) != 0 else client.address2,
                        address3=data['address3'] if len(data['address3']) != 0 else client.address3,
                        client_type=client_type if len(data['bnr_classification']) != 0 else client.client_type,
                    )
                    message = {'Success': 'Client information has been updated successfully in AIMS '}
                    return Response(message, status=status.HTTP_200_OK)
                except Exception as e:
                    message = {'Detail': 'Client update failed'}
                    return Response(message, status=status.HTTP_400_BAD_REQUEST)

        else:
            message = {'error': 'Client update failed . Client information not available in AIMS'}
            return Response(message, status=status.HTTP_404_NOT_FOUND)
    else:
        client_errors = []
        count = 1

        for error in errors:
            client_errors.append({count: error})
            count += 1
        return Response(client_errors, status=status.HTTP_400_BAD_REQUEST)





class MemberViewSet(viewsets.ModelViewSet):
    queryset = Membermaster.objects.all()
    serializer_class = MembermasterSerializer


class MemberUploadViewSet(viewsets.ModelViewSet):
    queryset = MemberupdNew.objects.all()
    serializer_class = MemberUploadSerializer


@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def get_loans(request):
    try:
        loans = Glmploan.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 100
        result_page = paginator.paginate_queryset(loans, request)
        serializer = LoanSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    except Exception as e:
        return Response(e, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_loan_detail(request, policy_no, member_no, loan_no):
    try:
        loan = Glmploan.objects.get(policy_no=policy_no, member_no=member_no, loan_no=loan_no)
        serializer = LoanSerializer(loan, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(e, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_joint_members(request):
    try:
        joint_members = Gljointmst.objects.all()
        serializer = JointMemberSerializer(joint_members,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except Exception as e:
        message = {'error': 'errors in loading joint members information'}
        return Response(e,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_joint_member(request,client_no):
    try:
        joint_member = Gljointmst.objects.get(client_no__contains=client_no)
        serializer = JointMemberSerializer(joint_member,many=False)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except Exception as e:
        message = {'error': 'errors in loading joint member information'}
        return Response(message,status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_joint_member(request):
    try:
        data = request.data
        errors = validate_joint_member(data)
        print("Testing joint member creation!")

        if len(errors) == 0:
            if Gljointmst.objects.filter(client_no__contains=data['client_no']).count() == 0:
                joint = Gljointmst.objects.create(
                    policy_no=data['policy_no'],
                    client_no=data['client_no'],
                    #member_no=data['member_no'],
                    loan_no=data['loan_no'],
                    surname=data['surname'],
                    other_names=data['other_names'],
                    title=data['title'],
                    status=data['status'],
                    commence_date=data['commence_date'],
                    birth_date=data['birth_date'],
                    age=data['age'],
                    marital_sta=data['marital_sta'],
                    principle_m=data['principle_m'],
                    loan_amount=float(data['loan_amount'])
                )
                message = {
                    'success': 'The joint member has been created successfully',
                    'client_no': data['client_no']
                }
                return Response(message, status=status.HTTP_200_OK)
        else:
            joint_errors = []
            count = 1
            for error in errors:
                joint_errors.append({count: error})
                count += 1
            return Response(joint_errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        message = {'error': 'errors in post data '}
        return Response(e, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_loan(request):
    try:
        data = request.data
        print('Testinga')
        errors = validate_loan_errors(data)

        if len(errors) == 0:

            commence_date = datetime.strptime(data['commence_date'], '%d/%m/%Y')
            loan_no = 0
            loan_no = Glmploan.objects.filter(policy_no=data['policy_no'], client_no=data['client_no']).count() + 1

            if Glmploan.objects.filter(policy_no=(data['policy_no']).strip(), client_no=(data['client_no']).strip(),
                                       uw_year=data['uw_year'], commence_date=commence_date).count() == 0:

                
                commence_date = datetime.strptime(data['commence_date'], '%d/%m/%Y')
                currentTimeDate = commence_date + relativedelta(months=int(data['term_months']))
                redemption_date = currentTimeDate.strftime('%Y-%m-%d')

                loan = Glmploan.objects.create(
                    policy_no=(data['policy_no']).strip(),
                    client_no=(data['client_no']).strip(),
                    member_no=data['member_no'],
                    uw_year=data['uw_year'],
                    loan_no=loan_no,
                    commence_date=commence_date,
                    joint_loan=data['joint_loan'],
                    total_sum_assured=float(data['loan_amount']),
                    mod_factor=data['mod_factor'],
                    interest_basis=data['interest_basis'],
                    age=data['age'],
                    term_months=data['term_months'],
                    term_years=data['term_years'],
                    interest_rate=float(data['interest_rate']),
                    annual_prem_rate=float(data['annual_prem_rate']),
                    lc_norm_annual_prem=float(data['premium']),
                    prorated_prem=float(data['prorated_prem']),
                    loan_premium=float(data['total_premium']),
                    admin_charge=float(data['admin_charge']),
                    crm_flag='Y',
                    redemtion_date=redemption_date,
                    rider_premium=float(data['rider_premium']),
                    rider_benefit=float(data['rider_benefit']),
                    comm_premium=float(data['comm_premium']),
                    status=1,
                    dola=date_time
                )
                message = {
                    'success': 'The loan has been created successfully',
                    'loan_no': loan_no
                }
                return Response(message, status=status.HTTP_200_OK)
            else:
                message = {'error': 'The loan already exist in AIMS'}
                return Response(message, status=status.HTTP_200_OK)
        else:
            loan_errors = []
            count = 1
            for error in errors:
                loan_errors.append({count: error})
                count += 1
            return Response(loan_errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response(e, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_loan(request, policy_no, member_no, loan_no):
    try:
        data = request.data
        errors = validate_loan_errors(request, data)

        if len(errors) == 0:

            commence_date = datetime.strptime(data['commence_date'], '%d/%m/%Y')
            currentTimeDate = commence_date + relativedelta(months=int(data['term_months']))
            redemption_date = currentTimeDate.strftime('%Y-%m-%d')
            
            print(data['admin_charge'])

            if Glmploan.objects.filter(policy_no=policy_no, member_no=member_no, loan_no=loan_no,
                                       commence_date=commence_date).count() > 0:

                update_loan = Glmploan.objects.filter(policy_no=policy_no, member_no=member_no, loan_no=loan_no,
                                                      commence_date=commence_date).update(
                    policy_no=(data['policy_no']).strip(),
                    client_no=(data['client_no']).strip(),
                    member_no=(data['member_no']).strip(),
                    uw_year=data['uw_year'],
                    # loan_no=loan_no,
                    commence_date=commence_date,
                    joint_loan=data['joint_loan'],
                    total_sum_assured=data['loan_amount'],
                    mod_factor=data['mod_factor'],
                    interest_basis=data['interest_basis'],
                    age=data['age'],
                    term_months=data['term_months'],
                    term_years=data['term_years'],
                    interest_rate=data['interest_rate'],
                    annual_prem_rate=data['annual_prem_rate'],
                    lc_norm_annual_prem=data['premium'],
                    prorated_prem=data['prorated_prem'],
                    loan_premium=data['total_premium'],
                    admin_charge=data['admin_charge'],
                    crm_flag='Y',
                    redemtion_date=redemption_date,
                    rider_premium=data['rider_premium'],
                    rider_benefit=data['rider_benefit'],
                    comm_premium=data['comm_premium'],
                    status=1,
                    dola=date_time
                )
                message = {
                    'success': 'The loan has been successfully updated in AIMS',
                    'loan_no': loan_no
                }
                return Response(message, status=status.HTTP_200_OK)
            else:
                message = {'error': 'The loan number does not exists in AIMS '}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)

        else:
            loan_errors = []
            count = 1
            for error in errors:
                loan_errors.append({count: error})
                count += 1
            return Response(loan_errors, status=status.HTTP_400_BAD_REQUEST)


    except Exception as e:
        return Response(e, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_riders(request):
    try:
        riders = Glmmridtl.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 100
        result_page = paginator.paginate_queryset(riders, request)
        serializer = RiderSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    except Exception as e:
        return Response(e, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_rider(request):
    try:
        data = request.data
        errors = validate_riders(data)

        if len(errors) == 0:
            if Glmmridtl.objects.filter(policy_no=str(data['policy_no']).strip(),uw_year=data['uw_year'],member_no=data['member_no'],
                                        rider_code=data['rider_code'],loan_no=data['loan_no']).count() == 0:
                rider = Glmmridtl.objects.create(
                    policy_no=data['policy_no'],
                    member_no=data['member_no'],
                    client_no=data['client_no'],
                    loan_no=data['loan_no'],
                    rider_code=data['rider_code'],
                    benefit=data['benefit'],
                    rate=data['rate'],
                    premium=data['premium'],
                    uw_year=data['uw_year'],
                    retrenchment=data['retrenchment'],
                    principal_yn=0,
                    retrenchment_period=data['retrenchment_period']
                )
                message = {'success': 'The rider has been created successfully in AIMS'}
                return Response(message, status=status.HTTP_201_CREATED)
            else:
                message = {'error': 'The rider already exists'}
                return Response(message,status=status.HTTP_400_BAD_REQUEST)


        else:
            rider_errors = []
            count = 1
            for error in errors:
                rider_errors.append({count: error})
                count += 1
            return Response(rider_errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(e, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_rider_life(request, policy_no, member_no, uw_year, rider_code):
    try:
        data = request.data
        errors = validate_riders(data)
        if len(errors) == 0:
            if Glmmridtl.objects.filter(policy_no=policy_no, member_no=member_no, uw_year=uw_year).count() > 0:
                update_rider = Glmmridtl.objects.filter(policy_no=policy_no, member_no=member_no,
                                                        uw_year=uw_year, rider_code=rider_code).update(
                    # policy_no=data['policy_no'],
                    # member_no=data['member_no'],
                    # client_no=data['client_no'],
                    # loan_no=data['loan_no'],
                    # rider_code=data['rider_code'],
                    benefit=data['benefit'],
                    rate=data['rate'],
                    premium=data['premium'],
                    retrenchment=data['retrenchment'],
                    retrenchment_period=data['retrenchment_period']

                )
                message = {'success': 'The rider has been updated successfully'}
                return Response(message, status=status.HTTP_200_OK)
            else:
                message = {'error': 'The rider does not exist in AIMS'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            rider_errors = []
            count = 1
            for error in errors:
                rider_errors.append({count: error})
                count += 1
            return Response(rider_errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(e, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_rider_credit(request, policy_no, member_no, loan_no, uw_year, rider_code):
    try:
        data = request.data
        errors = validate_riders(data)

        if len(errors) == 0:
            if Glmmridtl.objects.filter(policy_no=policy_no, member_no=member_no, loan_no=loan_no,
                                        uw_year=uw_year, rider_code=rider_code).count() > 0:

                update_rider = Glmmridtl.objects.filter(policy_no=policy_no, member_no=member_no, loan_no=loan_no,
                                                        uw_year=uw_year, rider_code=rider_code).update(
                    # policy_no=data['policy_no'],
                    # ember_no=data['member_no'],
                    # client_no=data['client_no'],
                    # loan_no=data['loan_no'],
                    # rider_code=data['rider_code'],
                    benefit=data['benefit'],
                    rate=data['rate'],
                    premium=data['premium'],
                    retrenchment=data['retrenchment'],
                    retrenchment_period=data['retrenchment_period']

                )
                message = {'success': 'The rider has been updated successfully'}
                return Response(message, status=status.HTTP_200_OK)
            else:
                message = {'Detail': 'The rider does not exist in AIMS'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            rider_errors = []
            count = 1
            for error in errors:
                rider_errors.append({count: error})
                count += 1
            return Response(rider_errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response(e, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_health_records(request):
    try:
        paginator = PageNumberPagination()
        paginator.page_size = 100

        health_records = Glcrhealthq.objects.all()
        result_page = paginator.paginate_queryset(health_records, request)
        serializer = HealthSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    except Exception as e:
        return Response(e, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_health_record(request):
    try:
        errors = validate_health_records(request.data)
        data = request.data
        if len(errors) == 0:
            w_count = Glcrhealthq.objects.filter(policy_no=data['policy_no'],client_no=data['client_no'],loan_no=data['loan_no']).count()
            if w_count == 0 :
                health_record = Glcrhealthq.objects.create(
                    policy_no=data['policy_no'],
                    uw_year=data['uw_year'],
                    client_no=data['client_no'],
                    member_no=data['member_no'],
                    q1=data['q1'],
                    q1description=data['q1description'],
                    q2=data['q2'],
                    q2description=data['q2description'],
                    loan_no=data['loan_no'],
                    weight=data['weight'],
                    height=data['height']
                )
                message = {'success': 'Health record has been created successfully '}
                return Response(message, status=status.HTTP_201_CREATED)
            else:
                message = {'error' : 'Health record already exist in aims'}
                return Response(message,status=status.HTTP_400_BAD_REQUEST)

        else:
            health_errors = []
            count = 1
            for error in errors:
                health_errors.append({count: error})
                count += 1
            return Response(health_errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(e, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_health_record(request, policy_no, member_no, loan_no):
    try:
        data = request.data
        errors = validate_health_records(request.data)

        if len(errors) == 0:

            if Glcrhealthq.objects.filter(policy_no=policy_no, member_no=member_no, loan_no=loan_no,
                                          uw_year=data['uw_year']).count() > 0:
                health_record = Glcrhealthq.objects.filter(
                    policy_no=data['policy_no'], member_no=data['member_no'], loan_no=data['loan_no'],
                    uw_year=data['uw_year']
                ).update(
                    # policy_no=data['policy_no'],
                    # uw_year=data['uw_year'],
                    # client_no=data['client_no'],
                    # member_no=data['member_no'],
                    q1=data['q1'],
                    q1description=data['q1description'],
                    q2=data['q2'],
                    q2description=data['q2description'],
                    weight=data['weight'],
                    height=data['height']
                )
                message = {'success': 'Health record has been successfully updated '}
                return Response(message, status=status.HTTP_200_OK)
        else:
            health_errors = []
            count = 1
            for error in errors:
                health_errors.append({count: error})
                count += 1
            return Response(health_errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response(e, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_identities(request):
    try:
        identities = Glidentity.objects.all()
        serializer = IdentitySerializer(identities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(e, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_provinces(request):
    try:
        provinces = Provinces.objects.all()
        serializer = ProvinceSerializer(provinces, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(e, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_districts(request):
    try:
        districts = Districts.objects.all()
        serializer = DistrictSerializer(districts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(e, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_sectors(request):
    try:
        sectors = Sectors.objects.all()
        serializer = SectorsSerializer(sectors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(e, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cells(request):
    try:
        cells = Cells.objects.all()
        serializer = CellsSerializer(cells, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(e, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes(IsAuthenticated)
def get_villages(request):
    try:
        villages = Village.objects.all()
        serializer = VillagesSerializer(villages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(e, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_bnrcodes(request):
    try:
        bnrcodes = Bnrclassification.objects.all()
        serializer = BnrSerializer(bnrcodes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(e, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_maritals(request):
    try:
        maritals = Glmasta.objects.all()
        serializer = MaritalSerializer(maritals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(e, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_industries(request):
    try:
        industries = NaicsCodes.objects.all()
        serializer = IndustrySerializer(industries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(e, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_economic_subs(request):
    try:
        economic_subs = EconomicSubSectors.objects.all()
        serializer = EconomicSerializer(economic_subs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(e, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_relations(request):
    try:
        relations = Glrelation.objects.all()
        serializer = RelationSerializer(relations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(e, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_statuses(request):
    try:
        statuses = Glstatus.objects.all()
        serializer = StatusSerializer(statuses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(e, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_occupations(request):
    try:
        occupations = Occupation.objects.all()
        serializer = OccupationSerializer(occupations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(e, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_ridersparams(request):
    try:
        riderparams = Glriders.objects.all()
        serializer = RidersParamSerializer(riderparams, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(e, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_titles(request):
    try:
        titles = Gltitle.objects.all()
        serializer = TitleSerializer(titles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(e, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_countries(request):
    try:
        countries = Countryparam.objects.all()
        serializer = CountrySerializer(countries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(e, status=status.HTTP_400_BAD_REQUEST)


def addYears(d, years):
    try:
        # Return same day of the current year
        return d.replace(year=d.year + years)
    except ValueError:
        # If not same day, it will return other, i.e.  February 29 to March 1 etc.
        return d + (date(d.year + years, 1, 1) - date(d.year, 1, 1))
