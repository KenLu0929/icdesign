from django.db import models
from django.utils.translation import gettext_lazy as _


class GenderClass(models.TextChoices):
    MAN = '男', _('男')
    WOMAN = '女', _('女')


class DegreeClass(models.TextChoices):
    HIGH_SCHOOL = '高中', _('高中')
    SPECIALIST = '專科', _('專科')
    BACHELOR = '學士', _('學士')
    MASTER = '碩士', _('碩士')
    DOCTOR = '博士', _('博士')


class StatusSchoolClass(models.TextChoices):
    STUDY = '在學', _('在學')
    GRADUATE = '畢業', _('畢業')
    UNDERGRADUATE = '肄業', _('肄業')


class ExamsStatusClass(models.TextChoices):
    WAITING = '等待中', _('等待中')
    REJECTED = '拒絕', _('拒絕')
    APPROVED = '同意', _('同意')


class ExamsLevelClass(models.TextChoices):
    ELECTIVE = '學科', _('學科')
    PRACTICAL = '術科', _('術科')


# Create your models here.
class Users(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)
    # personal data
    ic_id = models.CharField(max_length=100, unique=True, null=True, verbose_name="身分證字號")
    ic_name = models.CharField(max_length=100, null=True, verbose_name="姓名")
    ic_pass = models.CharField(max_length=100, null=True, verbose_name="密碼")
    ic_gender = models.CharField(
        max_length=10,
        choices=GenderClass.choices,
        null=True,
        verbose_name="性別"
    )
    ic_email = models.CharField(max_length=100, unique=True, null=True, verbose_name="電子郵件")
    ic_address = models.CharField(max_length=100, null=True, verbose_name="郵寄地址")
    ic_bod = models.DateField(null=True, verbose_name="出生日期")  # Birth of Date
    ic_phone_no = models.CharField(max_length=100, null=True, verbose_name="手機號碼")
    ic_telephone = models.CharField(max_length=100, null=True, verbose_name="電話號碼")
    # education data
    ic_school = models.CharField(max_length=100, null=True, verbose_name="學校名稱")
    ic_status_school = models.CharField(max_length=100,
                                        choices=StatusSchoolClass.choices,
                                        null=True,
                                        verbose_name="就學狀態")
    ic_degree = models.CharField(max_length=100,
                                 choices=DegreeClass.choices,
                                 null=True,
                                 verbose_name="最高學歷")
    ic_company = models.CharField(max_length=100, null=True, verbose_name="公司名稱")
    ic_department = models.CharField(max_length=100, null=True, verbose_name="系所名稱")
    ic_service_department = models.CharField(max_length=100, null=True, verbose_name="服務部門")
    ic_job_position = models.CharField(max_length=100, null=True, verbose_name="職稱")
    ic_yearofexp = models.IntegerField(null=True, default=0, verbose_name="工作年資")
    # additional data
    # ic_graduated_status = models.IntegerField(null=True,default=0,verbose_name="")  # 0 = not started yet, 1 = on progress, 2 = graduated.
    last_login = models.IntegerField(null=True, verbose_name="上次登入")
    date_created = models.DateTimeField(auto_now_add=True, null=True, verbose_name="註冊日期")
    date_modified = models.DateTimeField(auto_now=True, null=True, verbose_name="修改日期")

    class Meta:
        ordering = ['last_login']
        managed = True
        verbose_name = "user"
        verbose_name_plural = "users"


class ExamLogs(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)
    exam_ticket_no = models.CharField(max_length=100, null=True, verbose_name="准考證號碼")
    admission_ticket_no = models.CharField(max_length=100, null=True, default="-", verbose_name="准考證號碼")
    exam_id = models.CharField(max_length=100, null=True, verbose_name="考試編號")
    ic_id = models.CharField(max_length=100, null=True)
    # user = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    exam_grade = models.CharField(max_length=5, null=True, default="-", verbose_name="考試成績")
    exam_minutes = models.CharField(max_length=5, null=True, default="-", verbose_name="考試時間")
    exam_status = models.CharField(max_length=100,
                                   choices=ExamsStatusClass.choices,
                                   null=True,
                                   default=ExamsStatusClass.WAITING,
                                   verbose_name="考試狀態")
    exam_finish = models.BooleanField(null=True, default=False, verbose_name="考試是否結束")
    exam_place = models.CharField(max_length=100, null=True, verbose_name="考試地點")
    exam_room = models.CharField(max_length=100, null=True, verbose_name="考場")
    date_created = models.DateTimeField(auto_now_add=True, null=True, verbose_name="考試創建日期")
    date_modified = models.DateTimeField(auto_now=True, null=True, verbose_name="考試修改日期")

    class Meta:
        ordering = ["date_created", "exam_status", "exam_grade"]
        managed = True
        verbose_name = "exam log"
        verbose_name_plural = "exam logs"


class Exams(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)
    exam_name = models.CharField(max_length=100, null=True, verbose_name="考試名稱")
    exam_id = models.CharField(max_length=100, unique=True, null=True, verbose_name="考試編號")
    exam_start_time = models.DateTimeField(null=True, verbose_name="開始時間")
    exam_end_time = models.DateTimeField(null=True, verbose_name="結束時間")
    exam_place = models.CharField(max_length=100, null=True, verbose_name="考試地點")
    # exam_prefix = models.CharField(max_length=100, null=True)
    exam_level = models.CharField(max_length=100,
                                  choices=ExamsLevelClass.choices,
                                  null=True, verbose_name="考試科目")
    exam_is_active = models.IntegerField(null=True, default=0, verbose_name="是否啟用")  # 0 = Not Active, 1 = Active
    exam_user_taken = models.IntegerField(null=True, default=0)  # 0 = Not Active, 1 = Active
    exam_prerequisite = models.CharField(max_length=100, null=True, default="-",
                                         verbose_name="考試門檻")  # string with separator ","
    date_created = models.DateTimeField(auto_now_add=True, null=True, verbose_name="創建日期")
    date_modified = models.DateTimeField(auto_now=True, null=True, verbose_name="變更日期")

    @property
    def _get_month_exam(self):
        return self.exam_start_time.strftime('%m')

    @property
    def _get_user_exam(self):
        return self.exam_user_taken

    class Meta:
        ordering = ['date_created', 'exam_start_time', 'exam_end_time']
        managed = True
        verbose_name = "exam"
        verbose_name_plural = "exams"


class News(models.Model):
    news_id = models.AutoField(primary_key=True)
    news_title = models.CharField(max_length=100, null=True, verbose_name="最新消息標題")
    news_body = models.CharField(max_length=500, null=True, verbose_name="內文")
    news_author = models.CharField(max_length=100, null=True, verbose_name="作者")
    news_is_active = models.IntegerField(null=True, default=1, verbose_name="狀態")  # 0 = Not Active, 1 = Active
    date_created = models.DateTimeField(auto_now_add=True, null=True, verbose_name="創建日期")
    date_modified = models.DateTimeField(auto_now=True, null=True, verbose_name="修改日期")

    class Meta:
        ordering = ['date_created']
        managed = True
        verbose_name = "news"
        verbose_name_plural = "news"


class Sponsorship(models.Model):
    sponsor_id = models.AutoField(primary_key=True)
    sponsor_name = models.CharField(max_length=200, null=True, verbose_name="企業名稱")
    sponsor_url = models.CharField(max_length=200, null=True, verbose_name="企業網址")
    date_created = models.DateTimeField(auto_now_add=True, null=True, verbose_name="創建日期")
    date_modified = models.DateTimeField(auto_now=True, null=True, verbose_name="修改日期")

    class Meta:
        ordering = ['date_created']
        managed = True
        verbose_name = "Sponsorship"
        verbose_name_plural = "Sponsorship"


class CounterExamsLogs(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_modified = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ['date_created']
