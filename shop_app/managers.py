from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **additional_fields):
        if not email:
            raise ValueError('Email is Required!')
        user = self.model(email=email.lower(), **additional_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **additional_fields):
        additional_fields.setdefault('is_staff', True)
        additional_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **additional_fields)