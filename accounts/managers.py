from django.contrib.auth.models import BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    def _create_user(self, email, first_name, last_name, is_email_verified,
                     is_staff, is_active, is_superuser, password,
                     **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('Email must be set')

        email = self.normalize_email(email)

        user = self.model(email=email,
                          first_name=first_name,
                          last_name=last_name,
                          is_email_verified=is_email_verified,
                          is_staff=is_staff,
                          is_active=True,
                          is_superuser=is_superuser,
                          last_login=now,
                          date_joined=now,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, first_name, last_name,
                    password=None, **extra_fields):

        return self._create_user(email=email,
                                 first_name=first_name,
                                 last_name=last_name,
                                 is_email_verified=False,
                                 is_staff=False,
                                 is_active=True,
                                 is_superuser=False,
                                 password=password,
                                 **extra_fields)

    def create_superuser(self, email, first_name, last_name,
                         password, **extra_fields):
        return self._create_user(email=email,
                                 first_name=first_name,
                                 last_name=last_name,
                                 is_email_verified=True,
                                 is_staff=True,
                                 is_active=True,
                                 is_superuser=True,
                                 password=password,
                                 **extra_fields)
