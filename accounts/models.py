from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager

# Create your models here.
class customeUserManager(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError("Email is required!")
        
        email=self.normalize_email(email)
        user=self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,email,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("super user must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("superuser must have is_superuser=True")

        return self.create_user(email,password,**extra_fields)

class Register(AbstractUser):
    username=None
    email=models.EmailField(unique=True)


    phone=models.CharField(max_length=50)
    role=models.CharField(max_length=20,default='user')
    is_suspend=models.BooleanField(default=False)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]

    objects=customeUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
