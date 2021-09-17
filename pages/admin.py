from django.contrib import admin
from django.utils.translation import ngettext
from django.contrib import messages
import csv
from django.http import HttpResponse, HttpResponseRedirect
from io import StringIO
from icdesign import utils
from django.db.models import Q
from django.urls import path
from .models import Users, ExamLogs, Exams, News, Sponsorship, CounterExamsLogs
from .queries import QueryUsers, QueryExams

# Register your models here.


admin.site.site_header = 'ICDesign Administration'
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

    @admin.action(description='Download marked data as CSV')
    def download_csv(self, request, queryset):
        f = StringIO()
        writer = csv.writer(f)
        writer.writerow(["ic_id", "ic_name", "ic_gender", "ic_email", "ic_address",
                         "ic_bod", "ic_phone_no", "ic_telephone", "ic_school",
                         "ic_status_school", "ic_degree", "ic_company", "ic_department",
                         "ic_service_department", "ic_job_position", "ic_yearofexp", "date_created"])

        for s in queryset:
            writer.writerow([s.ic_id, s.ic_name, s.ic_gender, s.ic_email, s.ic_address,
                             s.ic_bod, s.ic_phone_no, s.ic_telephone, s.ic_school,
                             s.ic_status_school, s.ic_degree, s.ic_company, s.ic_department,
                             s.ic_service_department, s.ic_job_position, s.ic_yearofexp, s.date_created])

        f.seek(0)
        response = HttpResponse(f, content_type='text/csv')
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

    @admin.action(description='Mark selected exams as ACTIVATED')
    def make_activated(self, request, queryset):
        updated = queryset.update(exam_is_active=1)
        self.message_user(request, ngettext(
            '%d exam was successfully marked as ACTIVATED.',
            '%d exams were successfully marked as ACTIVATED.',
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description='Mark selected exams as NOT ACTIVATED')
    def make_not_activated(self, request, queryset):
        updated = queryset.update(exam_is_active=0)
        self.message_user(request, ngettext(
            '%d exam was successfully marked as NOT ACTIVATED.',
            '%d exams were successfully marked as NOT ACTIVATED.',
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description='Download marked data as CSV')
    def download_csv(self, request, queryset):
        f = StringIO()
        writer = csv.writer(f)
        writer.writerow(["exam_name", "exam_id", "exam_start_time", "exam_end_time", "exam_place",
                         "exam_level", "exam_is_active", "exam_prerequisite",
                         "date_created", "date_modified"])

        for s in queryset:
            writer.writerow([s.exam_name, s.exam_id, s.exam_start_time, s.exam_end_time, s.exam_place,
                             s.exam_level, s.exam_is_active, s.exam_prerequisite,
                             s.date_created, s.date_modified])

        f.seek(0)
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=exams-report.csv'
        return response


class ExamLogsAdmin(admin.ModelAdmin):
    # print()
    change_list_template = "pages/pages_changelist.html"
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
        ]
        return my_urls + urls

    def generate_adtics(self, request):
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

    @admin.action(description='Mark selected logs as APPROVED')
    def make_approved(self, request, queryset):
        updated = queryset.update(exam_status='同意')
        self.message_user(request, ngettext(
            '%d log was successfully marked as APPROVED.',
            '%d logs were successfully marked as APPROVED.',
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description='Mark selected logs as REJECTED')
    def make_rejected(self, request, queryset):
        updated = queryset.update(exam_status='拒絕')
        self.message_user(request, ngettext(
            '%d log was successfully marked as REJECTED.',
            '%d logs were successfully marked as REJECTED.',
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description='Download marked data as CSV')
    def download_csv(self, request, queryset):
        f = StringIO()
        writer = csv.writer(f)
        writer.writerow(["exam_ticket_no", "admission_ticket_no", "exam_id", "ic_id", "exam_grade",
                         "exam_minutes", "exam_status", "exam_finish", "exam_place", "exam_room", "date_created"])

        for s in queryset:
            data = {"ic_id": s.ic_id}
            user = QueryUsers.users_get(data)
            writer.writerow([s.exam_ticket_no, s.admission_ticket_no, s.exam_id, s.ic_id, s.exam_grade,
                             s.exam_minutes, s.exam_status, s.exam_finish, s.exam_place, s.exam_room, s.date_created])

        f.seek(0)
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=exams-logs-report.csv'
        return response

    @admin.action(description='Download marked data as Exams Report')
    def download_exams_report(self, request, queryset):
        f = StringIO()
        writer = csv.writer(f)
        writer.writerow(["Date of Test", "Test ID", "Test Name", "Test Room", "Admission ticket number", "Name"])

        for s in queryset:
            user_data = {"ic_id": s.ic_id}
            user = QueryUsers.users_get(user_data)

            exam_data = {"exam_id": s.exam_id}
            exam = QueryExams.exams_get(exam_data)

            writer.writerow([exam.get("exam_start_time"), s.exam_id, exam.get("exam_name"),
                             s.exam_room, s.admission_ticket_no, user.get("ic_name")])

        f.seek(0)
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=exams-report.csv'
        return response

    @admin.action(description='Download marked data as Candidate Report')
    def download_candidate_report(self, request, queryset):
        f = StringIO()
        writer = csv.writer(f)
        writer.writerow(["Admission ticket number", "Test ID", "Test Name",
                         "Test Area", "Test room", "Test Date", "ID",
                         "Name", "Gender", "Date of Birth", "Email",
                         "Phone Number", "Address", "University",
                         "Major Courses", "Status", "Graduate Status",
                         "Company", "Department", "Position",
                         "Years of Experience", "Test Score", "Test Status"])

        for s in queryset:
            user_data = {"ic_id": s.ic_id}
            user = QueryUsers.users_get(user_data)

            exam_data = {"exam_id": s.exam_id}
            exam = QueryExams.exams_get(exam_data)
            test_status = "-"
            if s.exam_grade != "" and s.exam_grade != "-":
                if int(s.exam_grade) >= 70:
                    test_status = "PASS"
                else:
                    test_status = "FAIL"

            writer.writerow([s.admission_ticket_no, s.exam_id, exam.get("exam_name"),
                             exam.get("exam_place"), s.exam_room, exam.get("exam_start_time"), user.get("ic_id"),
                             user.get("ic_name"), user.get("ic_gender"), user.get("ic_bod"), user.get("ic_email"),
                             user.get("ic_phone_no"), user.get("ic_address"), user.get("ic_school"),
                             user.get("ic_department"), s.exam_status, user.get("ic_status_school"),
                             user.get("ic_company"), user.get("ic_department"), user.get("ic_job_position"),
                             user.get("ic_yearofexp"), s.exam_grade, test_status,
                             ])

        f.seek(0)
        response = HttpResponse(f, content_type='text/csv')
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
