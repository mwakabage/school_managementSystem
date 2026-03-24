from django.db.models.signals import post_save
from django.dispatch import receiver
from authentication.models import User
from .models import TeacherSubject

@receiver(post_save, sender=User)
def create_teacher(sender, instance, created, **kwargs):
    if created and instance.role == "TEACHER":
        TeacherSubject.objects.create(user=instance ,subject=None)