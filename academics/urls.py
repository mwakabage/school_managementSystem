from django.urls import path
from academics import views

urlpatterns = [
    path('years/', views.academic_year_list, name='academic_year_list'),
    path('years/add/', views.add_academic_year, name='add_academic_year'),

    path('classes/', views.classroom_list, name='classroom_list'),
    path('classes/add/', views.add_classroom, name='add_classroom'),

    path('subjects/', views.subject_list, name='subject_list'),
    path('subjects/add/', views.add_subject, name='add_subject'),

    path('teacher-subject/', views.teacher_subject_list, name='teacher_subject_list'),
    path('teacher-subject/add/', views.add_teacher_subject, name='add_teacher_subject'),
    
    path('assignments/', views.teacher_add_assignment, name='assignments'),
    path('results/', views.teacher_add_result, name='student_results'),
    
    path("assignment/edit/<int:pk>/", views.edit_assignment, name="edit_assignment"),
    path("assignment/delete/<int:pk>/", views.delete_assignment, name="delete_assignment"),

    path("result/edit/<int:pk>/", views.edit_result, name="edit_result"),
    path("result/delete/<int:pk>/", views.delete_result, name="delete_result"),
]