from .models import User,Profile
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserChangeForm

class UserForm(ModelForm):
  

    class Meta:
        model = User
        fields = ('first_name', 'middle_name', 'last_name', 'email','password','phone_number','national_number' ,
                  'year','year_of_study')

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your middle name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter year of studying'}),
            'year_of_study':forms.TextInput(attrs={'Class': 'form-control', 'placeholder':'Enter year of study'}),
            'password':forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        }),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
            'national_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your national number'}),

        }


class ProfileForm(UserChangeForm): 
    password=None
    class Meta:
        model = User
        fields = ("first_name","middle_name","last_name",'profile_image','bio',)