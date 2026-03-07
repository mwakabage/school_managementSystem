from django.db import models
from authentication.models import User  
from academics.models import ClassRoom
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="students")
    class_room = models.ForeignKey(ClassRoom, on_delete=models.SET_NULL, null=True,
                                  blank=True,)
    admission_number = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.user.email
