from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

class AccountManager(BaseUserManager):
    
    def create_user(self, email, password, firstname, lastname, country, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, firstname=firstname, lastname=lastname, country=country, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, firstname, lastname, country, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, firstname, lastname, country, **extra_fields)



class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    phone = models.CharField(max_length=15, null=True, blank=True)
    google_id = models.CharField(max_length=250, null=True, blank=True)
    auth_provider = models.CharField(max_length=10, default='email')


    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname', 'country']

    objects = AccountManager()

    def __str__(self):
        return self.email