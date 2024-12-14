from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class CustomUserManager(BaseUserManager):

    @staticmethod
    def email_validator(email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError("You must provide a valid email address")

    def validate_user(self, first_name, last_name, email):
        if not first_name:
            raise ValueError("Users must submit a first name")

        if not last_name:
            raise ValueError("Users must submit a last name")

        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError("Base User Account: An email address is required")

    def create_user(self, first_name, last_name, email, password, **extra_fields):
        self.validate_user(first_name, last_name, email)

        extra_fields.setdefault('is_staff', False)

        user = self.model(first_name=first_name, last_name=last_name, email=email, **extra_fields)

        user.set_password(password)
        user.save()

        return user

    def validate_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        if not extra_fields.get('is_staff'):
            raise ValueError("Superusers must have is_staff=True")

        if not password:
            raise ValueError("Superusers must have a password")

        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError("Admin Account: An email address is required")
        return extra_fields

    def create_superuser(self, first_name, last_name, email, password, **extra_fields):
        extra_fields = self.validate_superuser(email, password, **extra_fields)
        user = self.create_user(first_name, last_name, email, password, **extra_fields)
        user.save()

        return user
