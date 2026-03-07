from django.contrib import admin
from .models import Student

class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'admission_number', 'class_room', 'date_of_birth')
    search_fields = ('first_name', 'email', 'admission_number')
    list_filter = ('class_room',)
    readonly_fields = ('user',)  # prevent editing the linked user accidentally



admin.site.register(Student, StudentAdmin)
