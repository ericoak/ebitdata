from django.contrib import admin

# Register your models here.

from .models import Week, Environment, Month, Uptime_Week

admin.site.register(Week)
admin.site.register(Environment)
admin.site.register(Month)
admin.site.register(Uptime_Week)
