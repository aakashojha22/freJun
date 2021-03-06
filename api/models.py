from django.db import models



class Account(models.Model):
    auth_id = models.CharField(max_length=40, blank=True, null=True)
    username = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'account'

# Create your models here.
class PhoneNumber(models.Model):
    number = models.CharField(max_length=40, blank=True, null=True)
    account = models.ForeignKey(Account, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'phone_number'