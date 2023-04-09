from django.contrib import admin

from services.models import Plan, Service, Subscription


admin.site.register(Service)
admin.site.register(Plan)
admin.site.register(Subscription)
