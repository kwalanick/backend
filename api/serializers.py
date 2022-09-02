from rest_framework import serializers ,fields
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from uploads.models import Glclmast,Membermaster,MemberupdNew,Schememaster,Glmploan,Glcrhealthq,Glmmridtl,Glriders,Gljointmst
from clients.models import Provinces,Districts,Sectors,Cells,Village,Glidentity,Bnrclassification,\
    Glmasta,NaicsCodes,Glrelation,EconomicSubSectors,Glstatus,Countryparam,Occupation,Gltitle
from rest_framework import pagination


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id','_id','username','email','name','isAdmin']

    def get__id(self,obj):
        return obj.id

    def get_name(self,obj):
        name = obj.first_name+' '+obj.last_name
        if name == '':
            name = obj.email
        return name
    def get_isAdmin(self,obj):
        return obj.is_staff


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id','_id','username','email','name','isAdmin','token']

    def get_token(self,obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


class ClientSerializer(serializers.ModelSerializer):
    birth_date = serializers.DateField(allow_null=True,required=False)
    spourse_name = serializers.SerializerMethodField(read_only=False)
    surname = serializers.SerializerMethodField(read_only=False)
    other_names = serializers.SerializerMethodField(read_only=False)

    class Meta:
        model = Glclmast
        fields = ['client_no','bnr_classification','surname','other_names','resident_country','country_code','identity_card_no',
                  'id_doc','gender','marital_status','spourse_name','birth_date','birth_reg_village','residence_type',
                  'email','mobile_no','telephone',
                  'fax','occupation','naics_code','economic_sub_sector','relation_to_company_code',
                  'province','district','sector','cellule','village',
                  'contact','contact_position','contact_telephone',
                  'title'
                  ]
    def get_spourse_name(self,obj):
        return (obj.spourse_name).strip()
    def get_surname(self,obj):
        return (obj.surname).strip()
    def get_other_names(self,obj):
        return (obj.other_names).strip()

class SchemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schememaster
        fields = ['policy_no','scheme_name','scheme_type','uw_year','scheme_type','client_no','branch','agent','bank_code',
                  'start_date','renewalable_flag','renewal_date',
                  'period_from','period_to','pay_freq','pay_mode','status_code','retirement_age','tin_no','tin_reg_date',
                  'admin_fee','date_created','commission_rate','free_cover_limit','commission_rate','lc_factor','with_rider',
                  'br_ind','savings_yn','total_sum_assured','total_annual_salary','gross_premium','nett_premium',
                  ]


class MembermasterSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    monthly_salary = serializers.SerializerMethodField(read_only=False)
    premium = serializers.SerializerMethodField(read_only=False)
    total_premium = serializers.SerializerMethodField(read_only=False)
    #date_left = serializers.SerializerMethodField(read_only=True)
    join_date = fields.DateField(input_formats=['%d/%m/%Y'])

    class Meta:
        model= Membermaster
        fields = [
                  'status_code','policy_no','member_no','client_no','institute_client_number','payroll_no','join_date','maturity_date',
                  'employment_date','uw_date','created_date','dob','modified_date','modified_by','period_from','period_to','term_years',
                  'surname','first_name','other_names','name','gender','pay_freq','monthly_salary','annual_salary',
                  #'id_type','id_no','employer_contrib','employee_contrib','employer_contrib_amt','employee_contrib_amt',
                  'branch', 'agent', 'retirement_age','lc_cover_factor','total_sum_assured', 'est_loan_amount',
                  'rider_benefit','rider_premium','premium','age','uw_year',
                  'medical_req','annual_prem_rate','total_premium','account_year','account_month','comm_amount','comm_rate',
                  'received_premium','balance','loans_granted',
                  'dept_no', 'comm_rate', 'retrenchment', 'retrench_period',
                  'premium_review_date','acquisition_cost','non_insurance_prem','type_of_bus','co_insure','company_share',
                  'premium_due_date',
                  'marital_status','medical_uw_loading','uw_decision',
                  #'orig_sum_insured', 'restricted_sum_assured','user_str','topup','date_left',
                  #'deactivation_date', 'deactivated_by','canc_reason','acceptance_terms_issued'
                  ]

    def get_monthly_salary(self,obj):
        return obj.current_salary


    def get_name(self,obj):
        name = obj.surname+' '+obj.first_name
        if name == '':
            name = obj.surname
        return name

    def get_premium(self,obj):
        return obj.lc_norm_annual_prem

    def get_total_premium(self, obj):
        return obj.lc_total_annual_prem


class MemberUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = MemberupdNew
        fields = ['policy_no','id_number','fname','lname','full_name']


class JointMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gljointmst
        fields = ['policy_no','client_no','loan_no','surname','other_names','title','status',
                  'commence_date','birth_date','age','marital_sta','principle_m','loan_amount'
                  ]


class LoanSerializer(serializers.ModelSerializer):
    loan_amount = serializers.SerializerMethodField(read_only=False)
    premium = serializers.SerializerMethodField(read_only=False)
    total_premium = serializers.SerializerMethodField(read_only=False)
    loan_no = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Glmploan
        fields = ['policy_no','client_no','member_no','loan_no','commence_date','joint_loan','loan_amount',
                  'mod_factor','interest_basis','age','term_months','term_years','interest_rate','annual_prem_rate',
                  'premium','prorated_prem','total_premium','admin_charge','rider_premium','rider_benefit','comm_premium'
                  ]

    def get_loan_no(self,obj):
        return obj.loan_no

    def get_loan_amount(self,obj):
        return obj.total_sum_assured

    def get_premium(self,obj):
        return obj.lc_norm_annual_prem

    def get_total_premium(self,obj):
        return obj.loan_premium


class RiderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Glmmridtl
        fields = ['policy_no','uw_year','client_no','member_no','rider_code','benefit','rate','premium',
                  'retrenchment','retrenchment_period']


class HealthSerializer(serializers.ModelSerializer):

    class Meta:
        model = Glcrhealthq
        fields = ['policy_no','uw_year','member_no','client_no','loan_no','q1',
                  'q1description','q2','q2description','weight','height']


class IdentitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Glidentity
        fields = '__all__'


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provinces
        fields = ('province','province_name')


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = Districts
        fields = ('province','district','district_name')


class SectorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sectors
        fields = ('sector_code','sector_name','district_code')


class CellsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cells
        fields = ('cell_code','cell_name','sector_code')


class VillagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Village
        fields = ('village_code','village_name','cell_code','sector_code','district_code','province_code')


class BnrSerializer(serializers.ModelSerializer):
    bnr_code = serializers.SerializerMethodField(read_only=False)
    class Meta:
        model = Bnrclassification
        fields = ('bnr_code','bnr_descr')

    def get_bnr_code(self,obj):
        return str(obj.bnr_code).strip()


class MaritalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Glmasta
        fields = ('code','desc_str',)


class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = NaicsCodes
        fields = ('naics_code','naics_description')


class EconomicSerializer(serializers.ModelSerializer):
    class Meta:
        model = EconomicSubSectors
        fields = ('isic_code','isic_description',)


class RelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Glrelation
        fields = ('code','description')


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Glstatus
        fields = ('status_type','status_desc',)


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Countryparam
        fields = ('country_code','country_description','country_nationality')


class OccupationSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField(read_only=False)
    code= serializers.SerializerMethodField(read_only=False)
    class Meta:
        model = Occupation
        fields = ('code','description')


    def get_description(self,obj):
        return str(obj.description).strip()

    def get_code(self, obj):
        return str(obj.occup_code).strip()


class RidersParamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Glriders
        fields = ('code','description')


class TitleSerializer(serializers.ModelSerializer):
    title_code = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Gltitle
        fields = ('title_code','description')

    def get_title_code(self,obj):
        return str(obj.title_code).strip()
