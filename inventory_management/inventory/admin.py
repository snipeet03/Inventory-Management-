
from django.contrib import admin
from django.contrib.auth.models import User
from .models import ProjectType, ExardProduct

admin.site.register(ProjectType)
admin.site.register(ExardProduct)


