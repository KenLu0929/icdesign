from django.contrib import admin
from django.utils.translation import ngettext
from django.contrib import messages
import csv
import os
from django.http import HttpResponse, HttpResponseRedirect
from io import StringIO
from icdesign import utils
from django import forms
from django.db.models import Q
from django.shortcuts import render
from django.urls import path, reverse
from .models import Users, ExamLogs, Exams, News, Sponsorship, CounterExamsLogs, SettingApp
from .queries import QueryUsers, QueryExams, QueryExamsLogs
from tablib import Dataset

# Register your models here.


admin.site.site_header = 'ICDesign 後台管理系統' # ICDesign Administration
exclude_field = ["auto_increment_id", "ic_pass"]


class UsersAdmin(admin.ModelAdmin):
    # print()
    list_display = [field.name for field in Users._meta.get_fields() if field.name not in exclude_field]

    readonly_fields = ("last_login", "date_created", "date_modified", "ic_pass")
    search_fields = ("ic_id", "ic_name", "ic_company", "ic_school")

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    actions = ['download_csv']

    @admin.action(description='下載已選取的用戶資料(CSV檔)')
    def download_csv(self, request, queryset):
        """Download marked data as CSV

        Args:
            request (HttpRequest): http request
            queryset (any): marked data

        Returns:
            HttpResponse: http response
        """        

        f = StringIO()
        writer = csv.writer(f)

        # writer.writerow(["ic_id", "ic_name", "ic_gender", "ic_email", "ic_address",
        #                "ic_bod", "ic_phone_no", "ic_telephone", "ic_school",
        #                "ic_status_school", "ic_degree", "ic_company", "ic_department",
        #                "ic_service_department", "ic_job_position", "ic_yearofexp", "date_created"])

        writer.writerow(["身分證字號", "姓名", "性別", "電子郵件", "郵寄地址",
                        "出生日期", "手機號碼", "電話號碼", "學校名稱",
                        "就學狀態", "最高學歷", "公司名稱", "系所名稱",
                        "服務部門", "職稱", "工作年資", "註冊日期"])

        for s in queryset:
            # filter null data
            ic_phone_no_data = s.ic_phone_no
            ic_telephone_data = s.ic_telephone

            if s.ic_phone_no:
                ic_phone_no_data = "\'"+str(s.ic_phone_no)

            if s.ic_telephone:
                ic_telephone_data = "\'"+str(s.ic_telephone)
            
            writer.writerow([s.ic_id, s.ic_name, s.ic_gender, s.ic_email, s.ic_address,
                            s.ic_bod, ic_phone_no_data, ic_telephone_data , s.ic_school,
                            s.ic_status_school, s.ic_degree, s.ic_company, s.ic_department,
                            s.ic_service_department, s.ic_job_position, s.ic_yearofexp, s.date_created])

        f.seek(0)
        response = HttpResponse(f, content_type='text/csv', charset='utf-8-sig')
        response['Content-Disposition'] = 'attachment; filename=users-report.csv'
        return response


class ExamsAdmin(admin.ModelAdmin):
    # print()
    list_display = [field.name for field in Exams._meta.get_fields() if field.name not in exclude_field]

    readonly_fields = ("date_created", "date_modified")
    search_fields = ("exam_name", "exam_id", "exam_place")

    filter_horizontal = ()
    list_filter = ["exam_is_active", "exam_place", "exam_level"]
    fieldsets = ()

    actions = ['make_activated', 'make_not_activated', 'download_csv']

    @admin.action(description='將被選取的考試啟用')
    def make_activated(self, request, queryset):
        """Mark selected exams as ACTIVATED

        Args:
            request (HttpRequest): http request
            queryset (any): selected data
        """        

        updated = queryset.update(exam_is_active=1)
        self.message_user(request, ngettext(
            # '%d exam was successfully marked as ACTIVATED.',
            # '%d exams were successfully marked as ACTIVATED.',
            '%d 個考試被成功啟用.',
            '%d 個考試被成功啟用.',
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description='將被選取的考試關閉')
    def make_not_activated(self, request, queryset):
        """Mark selected exams as NOT ACTIVATED

        Args:
            request (HttpRequest): Http request
            queryset (any): selected data
        """        

        updated = queryset.update(exam_is_active=0)
        self.message_user(request, ngettext(
            # '%d exam was successfully marked as NOT ACTIVATED.',
            # '%d exams were successfully marked as NOT ACTIVATED.',
            '%d 個考試被成功關閉.',
            '%d 個考試被成功關閉.',
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description='下載已選取的考試資料(CSV檔)')
    def download_csv(self, request, queryset):
        """Download marked data as CSV

        Args:
            request (HttpRequest): http request
            queryset (any): marked data

        Returns:
            HttpResponse: http response
        """        

        f = StringIO()
        writer = csv.writer(f)

        # writer.writerow(["exam_name", "exam_id", "exam_start_time", "exam_end_time", "exam_place",
        #                "exam_level", "exam_is_active", "exam_prerequisite",
        #                "date_created", "date_modified"])

        writer.writerow(["考試名稱", "考試編號", "開始時間", "結束時間", "考試地點",
                        "考試科目", "是否啟用", "考試門檻",
                        "創建日期", "變更日期"])

        for s in queryset:
            writer.writerow([s.exam_name, s.exam_id, s.exam_start_time, s.exam_end_time, s.exam_place,
                            s.exam_level, s.exam_is_active, s.exam_prerequisite,
                            s.date_created, s.date_modified])

        f.seek(0)
        response = HttpResponse(f, content_type='text/csv', charset='utf-8-sig')
        response['Content-Disposition'] = 'attachment; filename=exams-report.csv'
        return response


class FileImportForm(forms.Form):
    file_score = forms.FileField()


class ExamLogsAdmin(admin.ModelAdmin):
    # print()
    change_list_template = "admin/pages_changelist.html"
    list_display = [field.name for field in ExamLogs._meta.get_fields() if field.name not in exclude_field]

    readonly_fields = ("date_created", "date_modified", "exam_ticket_no")
    search_fields = ("ic_id", "exam_id", "exam_place", "exam_ticket_no")

    filter_horizontal = ()
    list_filter = ["exam_finish", "exam_status"]
    fieldsets = ()

    actions = ['make_approved', 'make_rejected', 'download_candidate_report',
                'download_exams_report', 'download_csv']

    def get_urls(self):
        urls = super().get_urls()

        my_urls = [
            path('generate_admission_ticket/', self.generate_adtics),
            path('upload-score-csv/', self.upload_score),
        ]
        return my_urls + urls

    def upload_score(self, request):
        if request.method == "POST":

            file_object = request.FILES["file_score"]
            # print(file_object)

            if not file_object.name.endswith('.csv') and not file_object.name.endswith('.xls') \
                    and not file_object.name.endswith('.xlsx'):
                messages.warning(request, 'The wrong file type was uploaded. please upload csv or xls (xlsx) file.')
                return HttpResponseRedirect(request.path_info)

            _, file_extension = os.path.splitext(file_object.name)
            file_extension = file_extension.replace(".", "")
            # print(file_extension)

            data_record = Dataset().load(file_object.read(), format=file_extension)
            # data_record = load_workbook(filename=file_object.file)
            # print(data_record)
            for fields in data_record:
                if fields[0] != "":
                    # print(fields[0])
                    admission_ticket = str(fields[0]).strip().replace('.0', '')
                    if admission_ticket != "":
                        # print(admission_ticket)
                        #
                        # print(fields[3])
                        # print(fields[6])

                        self.model.objects.filter(
                            Q(admission_ticket_no=admission_ticket) & Q(exam_id=fields[3])
                        ).update(
                            exam_grade=str(fields[6]),
                            exam_finish=True
                        )
                        # print(test)

            url = reverse('admin:index')
            return HttpResponseRedirect(url)

        form = FileImportForm()
        data = {"form": form}
        return render(request, "admin/csv_upload.html", data)

    def generate_adtics(self, request):
        """_summary_

        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """        

        res = self.model.objects.filter(Q(admission_ticket_no="-") & Q(exam_status="同意"))
        mess = "Admission Ticket is generated."
        fail_update = []
        if len(res) <= 0:
            mess = "Can not generating Admission Ticket, please check again the data or approve some registration data."
        for a in res:
            tickets = utils.generate_admission_ticket(a.exam_id)
            if tickets == "-":
                fail_update.append(a.exam_ticket_no)
            else:
                # print(tickets)
                self.model.objects.filter(auto_increment_id=a.auto_increment_id).update(admission_ticket_no=tickets)

        if len(fail_update) > 0:
            list_exam_ticket_no = ", ".join(fail_update)
            mess = "this is row cannot generate the admission ticket: " + list_exam_ticket_no

        self.message_user(request, mess)
        return HttpResponseRedirect("../")

    @admin.action(description='將被選取的資料的考試狀態改成同意')    
    def make_approved(self, request, queryset):
        """Mark selected logs as APPROVED

        Args:
            request (HttpRequest): http request
            queryset (any): selected data
        """        

        updated = queryset.update(exam_status='同意')
        self.message_user(request, ngettext(
            # '%d log was successfully marked as APPROVED.',
            # '%d logs were successfully marked as APPROVED.',
            '%d 筆資料的的考試狀態已經成功更改為 同意',
            '%d 筆資料的的考試狀態已經成功更改為 同意',
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description='將被選取的資料的考試狀態改成拒絕')
    def make_rejected(self, request, queryset):
        """Mark selected logs as REJECTED

        Args:
            request (HttpRequest): http request
            queryset (any): selected data
        """        

        updated = queryset.update(exam_status='拒絕')
        self.message_user(request, ngettext(
            # '%d log was successfully marked as REJECTED.',
            # '%d logs were successfully marked as REJECTED.',
            '%d 筆資料的的考試狀態已經成功更改為 拒絕',
            '%d 筆資料的的考試狀態已經成功更改為 拒絕',
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description='下載已選取的報考資料(CSV檔)')
    def download_csv(self, request, queryset):
        """Download marked data as CSV

        Args:
            request (HttpRequest): http request
            queryset (any): marked data

        Returns:
            HttpResponse: http response
        """        

        f = StringIO()
        writer = csv.writer(f)

        # writer.writerow(["exam_ticket_no", "admission_ticket_no", "exam_id", "ic_id", "exam_grade",
        #                "exam_minutes", "exam_status", "exam_finish", "exam_place", "exam_room", "date_created"])

        writer.writerow(["報考編號", "准考證號碼", "考試編號", "身分證字號", "考試成績",
                        "考試時間", "考試狀態", "是否更換過考試", "考試是否結束", "考試地點", "考場", "考試創建日期"])

        for s in queryset:
            writer.writerow([s.exam_ticket_no, s.admission_ticket_no, s.exam_id, s.ic_id, s.exam_grade,
                            s.exam_minutes, s.exam_status, s.exam_change, s.exam_finish, s.exam_place, s.exam_room, s.date_created])

        f.seek(0)
        response = HttpResponse(f, content_type='text/csv', charset='utf-8-sig')
        response['Content-Disposition'] = 'attachment; filename=exams-logs-report.csv'
        return response

    @admin.action(description='下載已選取的考生與考試報表(CSV檔)')
    def download_exams_report(self, request, queryset):
        """Download marked data as Exams Report

        Args:
            request (Httprequest): http request
            queryset (any): marked data

        Returns:
            HttpResponse: http response
        """        

        f = StringIO()
        writer = csv.writer(f)

        # writer.writerow(["Date of Test", "Test ID", "Test Name", "Test Room", "Admission ticket number", "Name"])

        writer.writerow(["考試日期", "考試編號", "考試名稱", "考場", "准考證號碼", "考生姓名"])

        for s in queryset:
            user_data = {"ic_id": s.ic_id}
            user = QueryUsers.users_get(user_data)

            exam_data = {"exam_id": s.exam_id}
            exam = QueryExams.exams_get(exam_data)
    
            writer.writerow([exam.get("exam_start_time"), s.exam_id, exam.get("exam_name"),
                            s.exam_room, s.admission_ticket_no, user.get("ic_name")])

        f.seek(0)
        response = HttpResponse(f, content_type='text/csv', charset='utf-8-sig')
        response['Content-Disposition'] = 'attachment; filename=exams-and-users-report.csv'
        return response

    @admin.action(description='下載已選取的考生報表(CSV檔)')
    def download_candidate_report(self, request, queryset):
        """Download marked data as Candidate Report

        Args:
            request (HttpRequest): http request
            queryset (any): marked data

        Returns:
            HttpResponse: http response
        """        

        f = StringIO()
        writer = csv.writer(f)

        # writer.writerow(["Admission ticket number", "Test ID", "Test Name",
        #                "Test Area", "Test room", "Test Date", "ID",
        #                "Name", "Gender", "Date of Birth", "Email",
        #                "Phone Number", "Address", "University",
        #                "Major Courses", "Status", "Graduate Status",
        #                "Company", "Department", "Position",
        #                "Years of Experience", "Test Score", "Test Status"])

        writer.writerow(["准考證號碼", "考試編號", "考試名稱",
                        "考試地點", "考場", "考試時間", "身分證字號",
                        "姓名", "性別", "出生日期", "電子郵件",
                        "手機號碼", "郵寄地址", "學校名稱學校名稱",
                        "系所名稱", "考試狀態", "就學狀態",
                        "公司名稱", "服務部門", "職稱",
                        "工作年資", "考試成績", "考試結果"])

        # check grade
        for s in queryset:
            user_data = {"ic_id": s.ic_id}
            user = QueryUsers.users_get(user_data)

            exam_data = {"exam_id": s.exam_id}
            exam = QueryExams.exams_get(exam_data)
            test_status = "-"

            if s.exam_grade != "" and s.exam_grade != "-" and s.exam_grade != "缺考":
                # 2021 test 學科
                if s.exam_id == 'SS1002' or s.exam_id == 'SYC1003':
                    if float(s.exam_grade) >= 80:
                        test_status = "PASS"
                    else:
                        test_status = "FAIL"
                # 2021 test 術科
                elif s.exam_id == 'PS1002' or s.exam_id == 'PYC1003':
                    if float(s.exam_grade) >= 70:
                        test_status = "PASS"
                    else:
                        test_status = "FAIL"
                # 2022 test 初階學科
                elif s.exam_id == 'SLV1':
                    if float(s.exam_grade) >= 70:
                        test_status = "PASS"
                    else:
                        test_status = "FAIL"
                # 2022 test 進階學科
                elif s.exam_id == 'SLV2':
                    if float(s.exam_grade) >= 85:
                        test_status = "PASS"
                    else:
                        test_status = "FAIL"
                # 2022 test 術科
                elif s.exam_id == 'PLV1' or s.exam_id == 'PLV2':
                    if float(s.exam_grade) >= 70:
                        test_status = "PASS"
                    else:
                        test_status = "FAIL"
                
            # filter null data
            ic_phone_no_data = user.get("ic_phone_no")

            if ic_phone_no_data:
                ic_phone_no_data = "\'"+str(ic_phone_no_data)
            
            writer.writerow([s.admission_ticket_no, s.exam_id, exam.get("exam_name"),
                            exam.get("exam_place"), s.exam_room, exam.get("exam_start_time"), user.get("ic_id"),
                            user.get("ic_name"), user.get("ic_gender"), user.get("ic_bod"), user.get("ic_email"),
                            ic_phone_no_data, user.get("ic_address"), user.get("ic_school"),
                            user.get("ic_department"), s.exam_status, user.get("ic_status_school"),
                            user.get("ic_company"), user.get("ic_service_department"), user.get("ic_job_position"),
                            user.get("ic_yearofexp"), s.exam_grade, test_status,
                            ])

        f.seek(0)
        response = HttpResponse(f, content_type='text/csv', charset='utf-8-sig')
        response['Content-Disposition'] = 'attachment; filename=candidate-report.csv'
        return response


class NewsAdmin(admin.ModelAdmin):
    # print()
    list_display = [field.name for field in News._meta.get_fields() if field.name not in exclude_field]

    readonly_fields = ("date_created", "date_modified", "news_id")
    search_fields = ("news_title", "news_body", "news_author")

    filter_horizontal = ()
    list_filter = ["news_author"]
    fieldsets = ()


class SponsorshipAdmin(admin.ModelAdmin):
    # print()
    list_display = [field.name for field in Sponsorship._meta.get_fields() if field.name not in exclude_field]

    readonly_fields = ("date_created", "date_modified", "sponsor_id")
    search_fields = ("sponsor_name", "sponsor_url")

    filter_horizontal = ()
    list_filter = []
    fieldsets = ()


class CounterExamsLogsAdmin(admin.ModelAdmin):
    readonly_fields = ("date_created", "date_modified", "content", "auto_increment_id")

    filter_horizontal = ()
    list_filter = []
    fieldsets = ()


admin.site.disable_action('delete_selected')
admin.site.register(Users, UsersAdmin)
admin.site.register(Exams, ExamsAdmin)
admin.site.register(ExamLogs, ExamLogsAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Sponsorship, SponsorshipAdmin)
admin.site.register(CounterExamsLogs, CounterExamsLogsAdmin)
admin.site.register(SettingApp)
