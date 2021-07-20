from django.db import models
from django.db import connection
from django.utils import timezone


# Create your models here.


class User(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)
    ic_id = models.CharField(max_length=100, unique=True, null=True)
    ic_name = models.CharField(max_length=100, null=True)
    ic_pass = models.CharField(max_length=100, null=True)
    ic_gender = models.CharField(max_length=50, null=True)
    ic_email = models.CharField(max_length=100, null=True)
    ic_address = models.CharField(max_length=100, null=True)
    ic_phone_no = models.CharField(max_length=100, null=True)
    ic_telephone = models.CharField(max_length=100, null=True)
    ic_degree = models.CharField(max_length=100, null=True)
    ic_address = models.CharField(max_length=100, null=True)
    ic_department = models.CharField(max_length=100, null=True)
    ic_company = models.CharField(max_length=100, null=True)
    # ic_graduated_time = models.IntegerField(null=True)
    ic_graduated_status = models.IntegerField(null=True)  # 0 = not started yet, 1 = on progress, 2 = graduated.
    date_joined = models.IntegerField(null=True)
    last_login = models.IntegerField(null=True)
    date_created = models.IntegerField(null=True)
    date_modified = models.IntegerField(null=True)

    class Meta:
        ordering = ['last_login']


class Exams(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)
    exam_name = models.CharField(max_length=100, null=True)
    ic_id = models.CharField(max_length=100, null=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    exam_ticket_no = models.CharField(max_length=100, null=True)
    exam_id = models.CharField(max_length=100, null=True)
    exam_taken_time = models.IntegerField(null=True)
    exam_taken = models.BooleanField(null=True)
    exam_grade = models.CharField(max_length=5, null=True)
    exam_finish = models.BooleanField(null=True)
    exam_place = models.CharField(max_length=100, null=True)
    date_created = models.IntegerField(null=True)
    date_modified = models.IntegerField(null=True)

    class Meta:
        ordering = ['date_created']
