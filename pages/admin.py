from django.contrib import admin
from .models import Users, ExamLogs, Exams, News, Sponsorship

# Register your models here.


admin.site.site_header = 'ICDesign Administration'
exclude_field = ["auto_increment_id"]


class UsersAdmin(admin.ModelAdmin):
    # print()
    list_display = [field.name for field in Users._meta.get_fields() if field.name not in exclude_field]

    readonly_fields = ("last_login", "date_created", "date_modified", "ic_pass")
    search_fields = ("ic_id", "ic_name", "ic_company", "ic_school")

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class ExamsAdmin(admin.ModelAdmin):
    # print()
    list_display = [field.name for field in Exams._meta.get_fields() if field.name not in exclude_field]

    readonly_fields = ("date_created", "date_modified")
    search_fields = ("exam_name", "exam_id", "exam_place")

    filter_horizontal = ()
    list_filter = ["exam_is_active"]
    fieldsets = ()


class ExamLogsAdmin(admin.ModelAdmin):
    # print()
    list_display = [field.name for field in ExamLogs._meta.get_fields() if field.name not in exclude_field]

    readonly_fields = ("date_created", "date_modified", "exam_ticket_no")
    search_fields = ("ic_id", "exam_id", "exam_place", "exam_ticket_no")

    filter_horizontal = ()
    list_filter = ["exam_finish", "exam_status"]
    fieldsets = ()


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


admin.site.register(Users, UsersAdmin)
admin.site.register(Exams, ExamsAdmin)
admin.site.register(ExamLogs, ExamLogsAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Sponsorship, SponsorshipAdmin)
