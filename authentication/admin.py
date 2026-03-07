from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin

class UserAdminModel(UserAdmin):
    ordering=['id']
    search_fields=['last_name',]
    list_display=[
        'email','password','first_name','middle_name','last_name','national_number','phone_number','year',
        'profile_image','is_active','is_staff','is_superuser',
        'role', 'classroom','year_of_study'
    ]
    fieldsets=(
       
        (
        None,
        {
          'fields':('email','password','first_name','middle_name','last_name','year','national_number',
                    'profile_image','phone_number','is_active','is_staff',
                    'is_superuser','role','classroom','year_of_study','bio')
        },
        ),
    )
    add_fieldsets = (
        ( 
         None, 
         {
           "classes":('wide',),
           "fields": (
               "email","password1","password2",
               "first_name","middle_name","last_name","national_number",
               "phone_number","year","year_of_study","profile_image","is_active","is_staff","is_superuser",
               "classroom","role","groups","bio"
           ),
       },
         ),
   )
    def save_model(self, request, obj, form, change):
        # Convert empty string to None for year
        if obj.year == '':
            obj.year = None
        super().save_model(request, obj, form, change)

# Register your models here.
admin.site.register(User,UserAdminModel)