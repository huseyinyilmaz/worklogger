from django.contrib.auth.models import (AbstractBaseUser,
                                        AbstractUser,
                                        PermissionsMixin)
from django.db import models


# Create your models here.
class User(AbstractUser):
    """Comes with default django user models
    username
    first_name
    last_name
    email
    is_staff
    is_active
    date_joined"""
    pass
