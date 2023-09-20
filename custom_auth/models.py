from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLES = [("Teacher", "Teacher"), ("Student", "Student")]
    role = models.CharField(max_length=30, choices=ROLES, default="Student")
    is_banned = models.BooleanField(default=False)
    