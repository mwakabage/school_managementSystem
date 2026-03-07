from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **kwargs):
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_active', True)
     
        user = self.create_user(email, password, **kwargs)
        return user

# Permission model
class Permission(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Role model
class Role(models.Model):
    name = models.CharField(max_length=50)
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return self.name

# Custom User model
class User(AbstractBaseUser, PermissionsMixin):
    class UserRole(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        STUDENT = "STUDENT", "Student"
        TEACHER = "TEACHER", "Teacher"
        ACCOUNTANT = "ACCOUNTANT", "Accountant"

    first_name = models.CharField(max_length=250, blank=True, null=True)
    middle_name = models.CharField(max_length=250, blank=True, null=True)
    last_name = models.CharField(max_length=250, blank=True, null=True)
    email = models.EmailField(max_length=250, unique=True)
    role = models.CharField(max_length=50, choices=UserRole.choices,default="STUDENT")
    year_of_study = models.CharField(max_length=250, blank=True, null=True)
    year = models.IntegerField(blank=True,null=True)
    phone_number = models.CharField(max_length=250, blank=True, null=True)
    national_number = models.CharField(max_length=250, blank=True)
    bio = models.TextField(max_length=250, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_pics/', default='default.jpg', blank=True, null=True)
    classroom = models.ForeignKey(
        'academics.ClassRoom',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students'
    )
    REQUIRED_FIELDS=[]
    USERNAME_FIELD='email'

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()


    # PermissionsMixin handles groups and user_permissions, but we add related_name
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_set",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions_set",
        blank=True
    )

    def __str__(self):
        return self.email

    def has_permission(self, permission_code):
        from .permissions import ROLE_PERMISSIONS
        if self.role in ROLE_PERMISSIONS:
            return permission_code in ROLE_PERMISSIONS[self.role]
        return False

# Profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profile_pics/', default='default.jpg')

    def __str__(self):
        return self.user.email
