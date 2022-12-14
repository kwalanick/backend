# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Occupation(models.Model):
    job_code = models.CharField(max_length=4, blank=True, null=True)
    description = models.CharField(max_length=30, blank=True, null=True)
    rate = models.DecimalField(max_digits=13, decimal_places=2, blank=True, null=True)
    per = models.DecimalField(max_digits=13, decimal_places=2, blank=True, null=True)
    sp = models.CharField(max_length=1, blank=True, null=True)
    user1 = models.CharField(max_length=19, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'occupation'
