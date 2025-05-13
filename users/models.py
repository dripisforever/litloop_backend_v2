import json
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from rest_framework_simplejwt.tokens import RefreshToken
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

from users.managers import UserManager


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'uploaded_media/user_avatar/id{0}/{1}'.format(instance.id, filename)

class User(AbstractBaseUser, PermissionsMixin):
    username    = models.CharField(max_length=255, unique=True, db_index=True)
    email       = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active   = models.BooleanField(default=True)
    is_staff    = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    avatar      = models.FileField(upload_to=user_directory_path, default="")

    # likings = models.ManyToManyField("self", blank=True)
    # following = models.ManyToManyField("self", blank=True)
    # followers = models.ManyToManyField("self", blank=True)

    ## A user may have access to zero or more advertisers or publishers
    # advertisers = models.ManyToManyField(Advertiser, blank=True)
    # publishers = models.ManyToManyField(Publisher, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email


    # def posts_count(self):
    #     return self.posts.all().count()
    def likes_count(self):
        return self.likes.count()

    def views_count(self):
        return self.viewed.count()

    def posts_count(self):
        return self.posts.count()
    # def tokens(self):
    #     refresh_token = RefreshToken.for_user(self)

    #     return {
    #         'refresh': str(refresh_token),
    #         'access': str(refresh_token.access_token),
    #     }

    def access_token(self):
        refresh_token = RefreshToken.for_user(self)

        return str(refresh_token.access_token)

    def refresh_token(self):
        refresh_token = RefreshToken.for_user(self)

        return str(refresh_token)
