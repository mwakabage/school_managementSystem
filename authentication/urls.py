from django.urls import path
from django.contrib import admin
from authentication import views

urlpatterns = [
    path('',views.login_form,name='login'),
    path('register/',views.register_form,name='register-page'),
    path('logout/',views.logout_view,name='logout'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('profile/', views.edit_profile, name="edit_profile"),

]