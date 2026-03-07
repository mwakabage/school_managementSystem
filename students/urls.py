from django.urls import path
from django.contrib import admin
from students import views

urlpatterns = [
    path('sdashboard/',views.student_dashboard,name='student_dashboard'),
    path('results/', views.student_result,name="student_result"),
    path('home/', views.student_home,name="student_home"),
    path('assignments/', views.student_assignments, name='student_assignments'),

]