from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.hashers import make_password


class EmailUserManager(UserManager):
    """Custom User model with email as username.
    """

    def _create_user(self, email, password, **extra_fields):
        """Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError('An email must be set')

        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom User model.
    """
    email = models.EmailField(
        _('email address'), unique=True,
        error_messages={
            'unique': _("A user with that email already exists.")})
    username = models.CharField(_('username'), max_length=150, blank=True)

    objects = EmailUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

