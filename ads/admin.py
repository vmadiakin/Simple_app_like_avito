from django.contrib import admin
from .models import Ad


class AdAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Ad, AdAdmin)
