from django.db import models


class UserAddress(models.Model):
    id = models.AutoField(primary_key=True)  # Changed from IntegerField
    email = models.CharField(max_length=255, blank=True, null=True)
    signer_name = models.CharField(max_length=255, blank=True, null=True)
    telphone = models.CharField(max_length=255, blank=True, null=True)
    signer_address = models.CharField(max_length=255, blank=True, null=True)
    district = models.CharField(max_length=255, blank=True, null=True)
    default = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_address'