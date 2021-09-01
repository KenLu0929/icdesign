from django.contrib import admin
from django.utils.translation import ngettext
from django.contrib import messages
import csv
from django.http import HttpResponse
from io import StringIO

from .models import Users, ExamLogs, Exams, News, Sponsorship, CounterExamsLogs

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

    actions = ['make_activated', 'make_not_activated']

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
    list_display = [field.name for field in ExamLogs._meta.get_fields() if field.name not in exclude_field]

    readonly_fields = ("date_created", "date_modified", "exam_ticket_no")
    search_fields = ("ic_id", "exam_id", "exam_place", "exam_ticket_no")

    filter_horizontal = ()
    list_filter = ["exam_finish", "exam_status"]
    fieldsets = ()
    actions = ['make_approved', 'make_rejected']

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
                         "exam_minutes", "exam_status", "exam_finish", "exam_place", "date_created"])

        for s in queryset:
            writer.writerow([s.exam_ticket_no, s.admission_ticket_no, s.exam_id, s.ic_id, s.exam_grade,
                             s.exam_minutes, s.exam_status, s.exam_finish, s.exam_place, s.date_created])

        f.seek(0)
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=exams-logs-report.csv'
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


admin.site.register(Users, UsersAdmin)
admin.site.register(Exams, ExamsAdmin)
admin.site.register(ExamLogs, ExamLogsAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Sponsorship, SponsorshipAdmin)
admin.site.register(CounterExamsLogs, CounterExamsLogsAdmin)
