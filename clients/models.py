from django.db import models

# Create your models here.
class Glstatus(models.Model):
    status_type = models.IntegerField(blank=True, null=True)
    status_desc = models.CharField(max_length=20, blank=True, null=True)
    user1 = models.CharField(max_length=11, blank=True, null=True)
    #id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'glstatus'

class Gltitle(models.Model):
    title_code = models.CharField(max_length=4, blank=True, null=True)
    description = models.CharField(max_length=30, blank=True, null=True)
    rate = models.DecimalField(max_digits=13, decimal_places=2, blank=True, null=True)
    per = models.DecimalField(max_digits=13, decimal_places=2, blank=True, null=True)
    sp = models.CharField(max_length=1, blank=True, null=True)
    user1 = models.CharField(max_length=19, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gltitle'

class EconomicSubSectors(models.Model):
    isic_code = models.CharField(max_length=6, blank=True, null=True)
    isic_description = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'economic_sub_sectors'

class Glrelation(models.Model):
    code = models.CharField(max_length=1, blank=True, null=True)
    description = models.CharField(max_length=30, blank=True, null=True)
    user_str = models.CharField(max_length=33, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'glrelation'

class NaicsCodes(models.Model):
    naics_code = models.CharField(max_length=6, blank=True, null=True)
    naics_description = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'NAICS_CODES'

class Glmasta(models.Model):
    code = models.CharField(primary_key=True,max_length=3)
    desc_str = models.CharField(max_length=20, blank=True, null=True)
    user1 = models.CharField(max_length=11, blank=True, null=True)
    #id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'glmasta'

class Bnrclassification(models.Model):
    bnr_code = models.CharField(max_length=4, blank=True, null=True)
    bnr_descr = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bnrclassification'

class Glidentity(models.Model):
    identity_type = models.CharField(max_length=3, blank=True, null=True)
    description = models.CharField(max_length=24, blank=True, null=True)
    user1 = models.CharField(max_length=22, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'glidentity'

class ClientUpload(models.Model):
    bnr_classification = models.CharField(max_length=5, blank=True, null=True)
    salutation = models.CharField(max_length=10, blank=True, null=True)
    sname = models.CharField(max_length=50, blank=True, null=True)
    fname = models.CharField(max_length=50, blank=True, null=True)
    client_name = models.CharField(max_length=200, blank=True, null=True)
    country_code = models.CharField(max_length=10, blank=True, null=True)
    resident_country = models.CharField(max_length=10, blank=True, null=True)
    identity_type = models.CharField(max_length=20, blank=True, null=True)
    identity_card_no = models.CharField(max_length=20, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, blank=True, null=True)
    marital_status = models.CharField(max_length=1, blank=True, null=True)
    spouse_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    mobile_no = models.IntegerField(blank=True, null=True)
    residence_type = models.CharField(max_length=1, blank=True, null=True)
    occupation_code = models.CharField(max_length=10, blank=True, null=True)
    naics_code = models.CharField(max_length=10, blank=True, null=True)
    economic_sub_sector = models.CharField(max_length=10, blank=True, null=True)
    relation_to_company_code = models.CharField(max_length=10, blank=True, null=True)
    pob_province = models.CharField(max_length=50, blank=True, null=True)
    pob_district = models.CharField(max_length=50, blank=True, null=True)
    pob_sector = models.CharField(max_length=50, blank=True, null=True)
    pob_cell = models.CharField(max_length=50, blank=True, null=True)
    pob_village = models.CharField(max_length=50, blank=True, null=True)
    rdb_reg_no = models.CharField(max_length=20,blank=True, null=True)
    rdb_reg_date = models.DateField(blank=True, null=True)
    province = models.CharField(max_length=20, blank=True, null=True)
    district = models.CharField(max_length=20, blank=True, null=True)
    sector = models.CharField(max_length=20, blank=True, null=True)
    cell = models.CharField(max_length=20, blank=True, null=True)
    village = models.CharField(max_length=20, blank=True, null=True)
    contact = models.CharField(max_length=45, blank=True, null=True)
    contact_position = models.CharField(max_length=20, blank=True, null=True)
    contact_telephone = models.CharField(max_length=25, blank=True, null=True)
    address = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=20, blank=True, null=True)
    town = models.CharField(max_length=20, blank=True, null=True)
    fax = models.CharField(max_length=20, blank=True, null=True)
    batch_no = models.CharField(max_length=8, blank=True, null=True)

    def __str__(self):
        return self.client_name

    class Meta:
        db_table = 'ClientUpload'


class Provinces(models.Model):
    province = models.IntegerField(blank=True, null=True)
    province_name = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'provinces'

class Districts(models.Model):
    province = models.IntegerField(blank=True, null=True)
    district = models.CharField(max_length=10, blank=True, null=True)
    district_name = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'districts'

class Sectors(models.Model):
    sector_code = models.CharField(max_length=10, blank=True, null=True)
    sector_name = models.CharField(max_length=30, blank=True, null=True)
    district_code = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sectors'


class Cells(models.Model):
    cell_code = models.CharField(max_length=10, blank=True, null=True)
    cell_name = models.CharField(max_length=30, blank=True, null=True)
    sector_code = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cells'

class Village(models.Model):
    village_code = models.CharField(max_length=10, blank=True, null=True)
    village_name = models.CharField(max_length=50, blank=True, null=True)
    cell_code = models.CharField(max_length=10, blank=True, null=True)
    sector_code = models.CharField(max_length=10, blank=True, null=True)
    district_code = models.CharField(max_length=10, blank=True, null=True)
    province_code = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'village'


class Countryparam(models.Model):
    record_no = models.CharField(max_length=3, blank=True, null=True)
    country_code = models.CharField(max_length=4, blank=True, null=True)
    country_description = models.CharField(max_length=60, blank=True, null=True)
    country_nationality = models.CharField(max_length=200, blank=True, null=True)
    bnr_code = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'countryparam'


class Occupation(models.Model):
    occup_code = models.CharField(max_length=4, primary_key=True)
    description = models.CharField(max_length=30, blank=True, null=True)
    #rate = models.DecimalField(max_digits=13, decimal_places=2, blank=True, null=True)
    #per = models.DecimalField(max_digits=13, decimal_places=2, blank=True, null=True)
    #sp = models.CharField(max_length=1, blank=True, null=True)
    #user1 = models.CharField(max_length=19, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'occupations'



