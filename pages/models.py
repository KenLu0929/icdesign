from datetime import datetime

from django.utils import timezone
from django.db import models
from icdesign import utils
from django.utils import timezone
from icdesign import settings
from django.utils.translation import gettext_lazy as _


class GenderClass(models.TextChoices):
    MAN = 'man', _('male')
    WOMAN = 'woman', _('female')


# Create your models here.
class Users(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)
    # personal data
    ic_id = models.CharField(max_length=100, unique=True, null=True)
    ic_name = models.CharField(max_length=100, null=True)
    ic_pass = models.CharField(max_length=100, null=True)
    ic_gender = models.CharField(
        max_length=10,
        choices=GenderClass.choices,
        null=True
    )
    ic_email = models.CharField(max_length=100, null=True)
    ic_address = models.CharField(max_length=100, null=True)
    ic_bod = models.DateField(null=True)  # Birth of Date
    ic_phone_no = models.CharField(max_length=100, null=True)
    ic_telephone = models.CharField(max_length=100, null=True)
    # education data
    ic_school = models.CharField(max_length=100, null=True)
    ic_status_school = models.CharField(max_length=100, null=True)
    ic_degree = models.CharField(max_length=100, null=True)
    ic_company = models.CharField(max_length=100, null=True)
    ic_department = models.CharField(max_length=100, null=True)
    ic_service_department = models.CharField(max_length=100, null=True)
    ic_job_position = models.CharField(max_length=100, null=True)
    ic_yearofexp = models.IntegerField(null=True)
    # additional data
    ic_graduated_status = models.IntegerField(null=True, default=0)  # 0 = not started yet, 1 = on progress, 2 = graduated.
    last_login = models.IntegerField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_modified = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ['last_login']
        managed = True
        verbose_name = "user"
        verbose_name_plural = "users"


class ExamLogs(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)
    exam_ticket_no = models.CharField(max_length=100, null=True)
    exam_id = models.CharField(max_length=100, null=True)
    ic_id = models.CharField(max_length=100, null=True)
    # user = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    exam_grade = models.CharField(max_length=5, null=True)
    exam_finish = models.BooleanField(null=True, default=False)
    exam_place = models.CharField(max_length=100, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_modified = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ['date_created']
        managed = True
        verbose_name = "exam log"
        verbose_name_plural = "exam logs"


class Exams(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)
    exam_name = models.CharField(max_length=100, null=True)
    exam_id = models.CharField(max_length=100, unique=True, null=True)
    exam_start_time = models.DateTimeField(null=True)
    exam_end_time = models.DateTimeField(null=True)
    exam_place = models.CharField(max_length=100, null=True)
    exam_is_active = models.IntegerField(null=True, default=0) # 0 = Not Active, 1 = Active
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_modified = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ['date_created']
        managed = True
        verbose_name = "exam"
        verbose_name_plural = "exams"


class News(models.Model):
    news_id = models.AutoField(primary_key=True)
    news_title = models.CharField(max_length=100, null=True)
    news_body = models.CharField(max_length=100, null=True)
    news_author = models.CharField(max_length=100, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_modified = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ['date_created']
        managed = True
        verbose_name = "news"
        verbose_name_plural = "news"


class Sponsorship(models.Model):
    sponsor_id = models.AutoField(primary_key=True)
    sponsor_name = models.CharField(max_length=100, null=True)
    sponsor_url = models.CharField(max_length=100, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_modified = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ['date_created']
        managed = True
        verbose_name = "Sponsorship"
        verbose_name_plural = "Sponsorship"
