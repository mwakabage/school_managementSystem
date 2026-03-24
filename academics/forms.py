from django import forms
from .models import Notes

class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['subject', 'class_room', 'title', 'file', 'video']
            
            