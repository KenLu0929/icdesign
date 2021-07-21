from django.contrib import admin
from .models import Users, Exams, Announcements, News, Sponsorship
# Register your models here.


admin.site.site_header = 'ICDesign Administration'
admin.site.register(Users)
admin.site.register(Exams)
admin.site.register(Announcements)
admin.site.register(News)
admin.site.register(Sponsorship)
