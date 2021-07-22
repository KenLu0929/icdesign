from django.contrib import admin
from .models import Users, ExamLogs, Exams, News, Sponsorship
# Register your models here.


admin.site.site_header = 'ICDesign Administration'
admin.site.register(Users)
admin.site.register(Exams)
admin.site.register(ExamLogs)
admin.site.register(News)
admin.site.register(Sponsorship)
