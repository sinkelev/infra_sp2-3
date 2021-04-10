from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        USER = 'user', 'user'
        MODERATOR = 'moderator', 'moderator'
        ADMIN = 'admin', 'admin'

    role = models.TextField(choices=Role.choices, default=Role.USER)
    is_active = models.BooleanField(default=False)
    email = models.EmailField('email', unique=True)
    bio = models.TextField(
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        self.is_active = True
        if self.role == 'moderator':
            self.is_staff = True
        if self.role == 'admin':
            self.is_superuser = True
        super(User, self).save(*args, **kwargs)

    class Meta:
        ordering = ['email']
