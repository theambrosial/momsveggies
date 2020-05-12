import datetime
import random, os
from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,
    User)

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,10}$',
                             message="Phone number must be entered in the format: '+999999999'. Up to 10 digits allowed.")
class SiteUserManager(BaseUserManager):
    """Creates and saves a User with the given email, mobile, first_name, last_name  and password."""
    def create_user(self, email, mobile, first_name, last_name, password=None, is_staff=False, is_active=True,
                    is_admin=False,):
        if not mobile:
            raise ValueError('user must have a phone number')
        if not password:
            raise ValueError('user must have a password')

        user = self.model(
            email=email,
            password=password,
            mobile=mobile,
            first_name=first_name,
            last_name=last_name,

        )

        user.set_password(password)
        user.staff = is_staff
        user.admin = is_admin
        user.active = is_active
        user.save(using=self._db)
        return user

    def create_superuser(self, email, mobile, first_name, last_name, password=None):
        user = self.create_user(
            email=email,
            mobile=mobile,
            first_name=first_name,
            last_name = last_name,
            password=password,


        )
        user.is_admin = True
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, mobile, first_name, last_name, password=None):
        user = self.create_user(
            email=email,
            mobile=mobile,
            first_name=first_name,
            last_name = last_name,

            password=password,


        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def get_filename_ext(filepath):
        base_name = os.path.basename(filepath)
        name, ext = os.path.splitext(base_name)
        return name, ext

    def upload_image_path(instance, filename):
        # print(instance)
        # print(filename)
        new_filename = random.randint(1,39534654564)
        name,ext = instance.get_filename_ext(filename)
        final_filename = '{new_filename}{ext}'.format(new_filename = new_filename, ext=ext)
        return "profilepictures/{new_filename}/{final_filename}".format(
            new_filename=new_filename,
            final_filename=final_filename
        )


class SiteUser(AbstractBaseUser):
    mobile = models.CharField('Contact No',validators=[phone_regex], max_length=10, unique=True)
    email = models.EmailField('Email-id', max_length=255, unique=True)
    first_name=models.CharField('First Name',max_length=30)
    last_name=models.CharField('Last Name',max_length=30)
    password_text = models.CharField(max_length=20, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    auto_timedate = models.DateTimeField(default=timezone.now)

    objects = SiteUserManager()

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return self.first_name


    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    @is_staff.setter
    def is_staff(self, value):
        self._is_staff = value















