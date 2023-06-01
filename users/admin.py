from django.contrib import admin
from users.models import Location, User


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name',)


class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)


admin.site.register(Location, LocationAdmin)
admin.site.register(User, UserAdmin)
