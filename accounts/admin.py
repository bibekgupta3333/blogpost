from django.contrib import admin
from .models import Profile
# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ['user']
    list_display = ['user', 'phone']
