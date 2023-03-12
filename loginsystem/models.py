import os

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username

        )
        user.is_admin = True
        user.is_staff = True

        user.is_superuser = True
        user.save(using=self._db)
        return user


# new 13 Azar
# def get_profile_image_filepath(self,filename):
#     filename = str(self.image)[str(self.image).index('images/' + str(self.pk) + "/"):]
#     return 'images/'+str(self.pk)+filename

# def get_profile_image_filepath(instance, filename):
#     return '/'.join(['images/', instance.user.username, filename])
# def get_image_filepath(instance,filename):
#     return '/'.join(['user',instance.user.username,filename])

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'images/user_{0}/{1}'.format(instance.id, filename)
    # return 'user_{0}/{1}'.format(instance.email, filename)
#both of above return work true



class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=60,
        unique=True

    )
    username = models.CharField(max_length=50, default=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    phone_number = PhoneNumberField(unique=False, null=True, blank=True)
    fullname = models.CharField(max_length=70, blank=True)
    image = models.ImageField(upload_to= user_directory_path, blank=True, default="codingwithmelika/default_image.png")
    # image = models.ImageField(upload_to='images/', null=True, blank=True, default="codingwithmelika/default_image.png")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
