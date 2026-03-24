from django.urls import path
from django.contrib import admin
from students import views

urlpatterns = [
    path('sdashboard/',views.student_dashboard,name='student_dashboard'),
    path('results/', views.student_result,name="student_result"),
    path('home/', views.student_home,name="student_home"),
    path('assignment/', views.student_assignment, name="student_assignment"),
    path('student-materials/', views.student_materials, name="student_material"),
]