from django.utils.html import mark_safe
from django.db import models
from django.contrib.auth.models import User
from typing import Any
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username,phone_number, email, password=None):
        if not email:
            return ValueError('User must have an email address')
        if not username:
            return ValueError('User must have a username')
        
        user = self.model(

            email =  self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            phone_number=phone_number,
            


        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name, last_name, username, email, password):
        user = self.create_user(
           email =  self.normalize_email(email),
           username = username,
           password = password,
           first_name = first_name,
           last_name = last_name,
 
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_SuperAdmin = True
        user.save(using=self._db)
        return user

class account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=50)
    Date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True )
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_SuperAdmin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm , odj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True



class UserProfile(models.Model):
    user = models.OneToOneField(account, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    class Meta:
       verbose_name = 'UserProfile'
       verbose_name_plural = 'UserProfiles'

    def image_tag(self):
     if self.profile_picture and hasattr(self.profile_picture, 'url'):
        return mark_safe('<img src="%s" width="50" height="30" />' % (self.profile_picture.url))
     else:
         return "No Image Found"


    def __str__(self):
        return self.user.username
