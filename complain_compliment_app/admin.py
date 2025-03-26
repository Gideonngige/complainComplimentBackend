from django.contrib import admin
from . models import Users, Feedbacks,  AdminResponse, Report

# Register your models here
admin.site.register(Users)
admin.site.register(Feedbacks)
admin.site.register(AdminResponse)
admin.site.register(Report)
