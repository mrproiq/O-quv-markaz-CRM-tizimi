from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email kiritilishi shart")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser 'is_staff=True' bo'lishi kerak.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser 'is_superuser=True' bo'lishi kerak.")
        if not extra_fields.get("is_active"):
            raise ValueError("Agar 'is_active=True' qilmasangiz admin panelga kiraolmaysiz.")

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    class Roles(models.TextChoices):
        SUPERADMIN = "SUPERADMIN", "Super Admin"
        BOSS = "BOSS", "Boss"
        ADMIN = "ADMIN", "Admin"
        MENTOR = "MENTOR", "Mentor"

    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.MENTOR)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.username or self.email} {self.role}"




