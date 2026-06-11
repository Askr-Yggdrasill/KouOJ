from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        USER = "user", "用户"
        ADMIN = "admin", "管理员"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.USER)
    solved_count = models.PositiveIntegerField(default=0)
    submit_count = models.PositiveIntegerField(default=0)
    nickname = models.CharField(max_length=20, blank=True)
    avatar_url = models.URLField(blank=True)
    bio = models.TextField(max_length=200, blank=True)

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN or self.is_staff
