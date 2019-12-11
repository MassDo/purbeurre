from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUser(AbstractUser):
    
    # the field used for authenticate, it must be unique.
    email = models.EmailField(("email address"), blank=True, unique=True) # email is unique
    USERNAME_FIELD = 'email' 
    # fields for createsuperuser,in addition of default mendatory attributs username_field and password
    REQUIRED_FIELDS = ['username']
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return (f' Username: {self.username} Email: {self.email}')