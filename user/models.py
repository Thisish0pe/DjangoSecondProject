from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    
    def _create_user(self, username, password, nickname, is_staff, is_superuser, **extra_fields):
        if not username:
            raise ValueError('User must have a username')
        # now = timezone.now() # 현재시간 -> UTC
        now = timezone.localtime()
        user = self.model(
            username=username,
            nickname=nickname,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    # create_user
    def create_user(self, username, password, nickname, **extra_fields):
        return self._create_user(username, password, nickname, False, False, **extra_fields)
    # create_superuser
    def create_superuser(self, username, password, nickname, **extra_fields):
        return self._create_user(username, password, nickname, True, True, **extra_fields)


class User(AbstractUser):
    nickname = models.CharField(max_length=15)
    first_name = None
    last_name = None

    REQUIRED_FIELDS = ['nickname']

    objects = UserManager()

    def __str__(self):
        return self.nickname
