from django.db import models


class User(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    birthday = models.DateTimeField(blank=True, null=True)
    mobile = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True,unique=True)
    password = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'user'
