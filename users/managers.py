# https://chatgpt.com/c/681f1947-13f8-800c-a93c-9cd62aeeff58
# your_app/models/managers.py

from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self, username, email, password):
        if not email:
            raise TypeError('Users must have an email address')
        elif not username:
            raise TypeError('Users must have an username')
        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            email = email,
            username = username,
            password = password,
        )
        user.is_admin = True
        user.is_staff = True
        # user.has_perm = True
        user.save(using=self._db)
        return user
