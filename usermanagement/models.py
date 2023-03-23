from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionManager,PermissionsMixin
from django.core.validators import RegexValidator


# Create your models here.

class UserManager(BaseUserManager,PermissionManager):

    def create_user(self,phone,email=None,password=None,is_staff=False,is_active=True,is_superuser=False,**extra_fields):
        if  not phone:
            raise ValueError('users must have a phone number')
        if not password:
            raise ValueError('user must have a password')
        user_obj =self.model(
            phone =phone,
        )
        user_obj
        user_obj.email = email
        user_obj.set_password(password)
        user_obj.is_staff=is_staff
        user_obj.is_superuser = is_superuser
        user_obj.is_active =is_active
        user_obj
        user_obj.save(using=self._db)
        return user_obj


    def create_staffuser(self,phone,password=None):
        user =self.create_user(
            phone,
            password=password,
            is_staff=True,
        )
        return user

    def create_superuser(self,phone,password=None):
        user =self.create_user(
            phone,
            password=password,
            is_staff=True,
            is_superuser=True,
        )
        return user



class User(AbstractBaseUser,PermissionsMixin):
    phone_regex = RegexValidator(regex =r'^\+?1?\d{9,10}$',
        message = "Phone number must be entered in the format:'+99999999'.Up to 10 digits allowed.")    
    phone = models.CharField(validators=[phone_regex],max_length=17,unique=True)
    first_name = models.CharField(max_length=225)
    last_name = models.CharField(max_length=225, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = "phone"
    objects = UserManager()

    def __str__(self):
        return self.first_name


    
class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone_regex = RegexValidator(regex =r'^\+?1?\d{9,10}$',
        message = "Phone number must be entered in the format:'+99999999'.Up to 10 digits allowed.")    
    phone = models.CharField(validators=[phone_regex],max_length=17,unique=True)
    email = models.EmailField(max_length=100,unique=True)
    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'
    GENDER_OPTIONS = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other')
    ]
    gender = models.CharField(max_length=1,choices=GENDER_OPTIONS)

    def __str__(self) -> str:
        return self.name + " - " + self.phone 
