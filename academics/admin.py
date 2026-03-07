from django.contrib import admin
from .models import AcademicYear, ClassRoom, Subject, TeacherSubject, Assignment, Result


# Academic Year
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('year_of_study', 'active')
    list_filter = ('active',)
    search_fields = ('year_of_study',)


# Class Room
class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'stream')
    search_fields = ('name', 'stream')


# Subject
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code','class_room')
    search_fields = ('name', 'code')


# Teacher Subject
class TeacherSubjectAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'subject', 'classroom')
    list_filter = ('classroom',)
    search_fields = ('teacher__email', 'subject__name')

class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject','description', 'due_date', 'created_at','class_room')
    search_fields = ('title', 'subject__name')
    list_filter = ('subject', 'due_date')
    ordering = ('-created_at',)
    date_hierarchy = 'due_date'

class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'marks', 'grade', 'term', 'created_at','class_room')
    search_fields = ('student', 'subject', 'term')
    list_filter = ('term', 'subject')
    ordering = ('-created_at',)

admin.site.register(AcademicYear, AcademicYearAdmin)
admin.site.register(ClassRoom, ClassRoomAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(TeacherSubject, TeacherSubjectAdmin)
