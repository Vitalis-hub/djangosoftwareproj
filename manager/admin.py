from django.contrib import admin

# Register your models here.
from .models import Manager
from django.contrib.auth.models import Permission

# Register your models here.
admin.site.register(Manager)
admin.site.register(Permission)
