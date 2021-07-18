from django.db import models
from django.db import connection
from django.utils import timezone


# Create your models here.


class User(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)
    ic_id = models.CharField(max_length=100, unique=True, null=True)
    full_name = models.CharField(max_length=100, null=True)
    ic_pass = models.CharField(max_length=100, null=True)
    gender = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    phone_no = models.CharField(max_length=100, null=True)
    telephone = models.CharField(max_length=100, null=True)
    highest_degree = models.CharField(max_length=100, null=True)
    school_name = models.CharField(max_length=100, null=True)
    department_school = models.CharField(max_length=100, null=True)
    company_name = models.CharField(max_length=100, null=True)
    list_of_test = models.JSONField(default=None, null=True)
    date_joined = models.IntegerField(null=True)
    last_login = models.IntegerField(null=True)
    grade = models.CharField(max_length=5, null=True)

    class Meta:
        ordering = ['last_login']

