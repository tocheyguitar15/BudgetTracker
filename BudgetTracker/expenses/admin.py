from django.contrib import admin
from .models import Tracker
# Register your models here.
@admin.register(Tracker)
class TrackerAdmin(admin.ModelAdmin):
    list_display = ('uname','quote','cost')

# @admin.register(Users)
# class UsersAdmin(admin.ModelAdmin):
#     list_display = ('username', 'password')
    