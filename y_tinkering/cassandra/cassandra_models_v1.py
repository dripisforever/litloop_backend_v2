import tempfile

from django.db import models
from django.db.models.signals import m2m_changed, post_delete, post_save, pre_delete
from django.dispatch import receiver
from django.utils.html import strip_tags

from users.models import User
from photos.models import Photo
from videos.models import Video
from tracks.models import Track
from playlists.models import Playlist

from posts import helpers

def post_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'uploaded_media/post_images/post_id_{0}/{1}'.format(instance.id, filename)


class Post(models.Model):

    videos      = models.ManyToManyField(Video, through="PostVideo", blank=True)
    tracks      = models.ManyToManyField(Track, through="PostTrack", blank=True)
    photos      = models.ManyToManyField(Photo, through="PostPhoto", blank=True)
    playlists   = models.ManyToManyField(Playlist, through="PostPlaylist", blank=True)

    title       = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=100, blank=True)
    friendly_id = models.CharField(max_length=100, blank=True)

    author      = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    caption     = models.CharField(max_length=50, blank=True)
    image       = models.FileField(upload_to=post_directory_path, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    likes       = models.ManyToManyField(User, through='PostLike', blank=True, related_name='post_likes')
    dislikes    = models.ManyToManyField(User, through='PostDislike', blank=True, related_name='post_dislikes')
    views       = models.ManyToManyField(User, through='PostView', blank=True, related_name='post_views')
    impressions = models.ManyToManyField(User, through='PostImpression', blank=True, related_name='post_impressions')

    # likes       = models.ManyToManyField(User, through='PostLike', blank=True, related_name='likes')
    # dislikes    = models.ManyToManyField(User, through='PostDislike', blank=True, related_name='dislikes')
    # views       = models.ManyToManyField(User, through='PostView', blank=True, related_name='views')
    # impressions = models.ManyToManyField(User, through='PostImpression', blank=True, related_name='impressions')

    class Meta:
        ordering: ['-updated_at']


    def __str__(self):
        return self.caption

    @property
    def total_likes(self):
        return self.likes.count()

    def likes_count(self):
        return self.likes.count()

    def views_count(self):
        return self.views.count()

    def save(self, *args, **kwargs):
        strip_text_items = ["title", "description"]
        for item in strip_text_items:
            setattr(self, item, strip_tags(getattr(self, item, None)))
        self.title = self.title[:99]

        if not self.friendly_id:
            while True:
                friendly_id = helpers.produce_friendly_token()
                if not Post.objects.filter(friendly_id=friendly_id):
                    self.friendly_id = friendly_id
                    break
        super(Post, self).save(*args, **kwargs)



class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class PostDislike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class PostImpression(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class PostView(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)



class PostPhoto(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    photo = models.ForeignKey('photos.Photo', on_delete=models.CASCADE)
    order = models.IntegerField(default=1)

class PostVideo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    video = models.ForeignKey('videos.Video', on_delete=models.CASCADE)
    order = models.IntegerField(default=1)

class PostTrack(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    track = models.ForeignKey('tracks.Track', on_delete=models.CASCADE)
    order = models.IntegerField(default=1)

class PostPlaylist(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    playlist = models.ForeignKey('playlists.Playlist', on_delete=models.CASCADE)
    order = models.IntegerField(default=1)


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

    followers   = models.ManyToManyField("self", through=Follow, blank=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following_relation', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='follower_relation', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower} follows {self.following}"


class GroupChat(models.Model):
    name = models.SlugField(max_length=20)
    description = models.CharField(blank=True)
    members = models.ManyToManyField(User, related_name='group_chats')
    # messages = models.ManyToManyField(Message, blank=True )

class Message(models.Model):
    parent_group = models.ForeignKey(GroupChat, on_delete=models.CASCADE, related_name="messages")
    parent_user = models.ForeignKey(User, on_delete=models.SET(get_sentinal_user))

    # groupchat = models.ForeignKey(GroupChat, on_delete=models.CASCADE, related_name='messages')
    # sender = models.ForeignKey(User, on_delete=models.CASCADE)
    # content = models.TextField(blank=True)

    message_text = models.TextField(blank=True)
    date_posted = models.DateTimeField(default=timezone.localtime().now)
    videos = models.ManyToManyField(Video, related_name='messages', blank=True)
    photos = models.ManyToManyField(Photo, related_name='messages', blank=True)
    tracks = models.ManyToManyField(Track, related_name='messages', blank=True)
    attachments = models.ManyToManyField(Attachment, blank=True)


import uuid

from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit

from posts.helpers import original_media_file_path, original_thumbnail_file_path
from users.models import User

class Photo(models.Model):
    s3_key          = models.CharField(max_length=400, null=True)
    filename        = models.CharField(max_length=400, null=True)

    user            = models.ForeignKey("users.User", on_delete=models.CASCADE)
    title           = models.TextField(blank=True, null=True)
    photo_file      = models.FileField(upload_to="media_files/photos/")

    user_featured   = models.BooleanField(default=False)
    friendly_token  = models.CharField(blank=True, max_length=12, db_index=True)

    likes           = models.ManyToManyField(User, through='PhotoLike', blank=True, related_name='photo_likes')
    dislikes        = models.ManyToManyField(User, through='PhotoDislike', blank=True, related_name='photo_dislikes')
    views           = models.ManyToManyField(User, through='PhotoView', blank=True, related_name='photo_views')
    impressions     = models.ManyToManyField(User, through='PhotoImpression', blank=True, related_name='photo_impressions')


class PhotoLike(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    liked_by = models.ForeignKey('users.User', on_delete=models.CASCADE)

class PhotoDislike(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    dislike_by = models.ForeignKey('users.User', on_delete=models.CASCADE)

class PhotoImpression(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)

class PhotoView(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)


class PhotoAlbum(models.Model):
    """PhotoAlbums model"""

    add_date = models.DateTimeField(auto_now_add=True, db_index=True)
    description = models.TextField(blank=True, help_text="description")
    friendly_token = models.CharField(blank=True, max_length=12, db_index=True)
    photo = models.ManyToManyField(Photo, through="PhotoAlbumItem", blank=True)
    title = models.CharField(max_length=100, db_index=True)
    uid = models.UUIDField(unique=True, default=uuid.uuid4)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, db_index=True, related_name="photoalbums")

    def __str__(self):
        return self.title

    @property
    def photo_count(self):
        return self.photo.count()

    def get_absolute_url(self, api=False):
        if api:
            return reverse("api_get_photoalbum", kwargs={"friendly_token": self.friendly_token})
        else:
            return reverse("get_playlist", kwargs={"friendly_token": self.friendly_token})

    @property
    def url(self):
        return self.get_absolute_url()

    @property
    def api_url(self):
        return self.get_absolute_url(api=True)

    def user_thumbnail_url(self):
        if self.user.logo:
            return helpers.url_from_path(self.user.logo.path)
        return None

    def set_ordering(self, photo, ordering):
        if photo not in self.photo.all():
            return False
        pa = PhotoAlbum.objects.filter(photo_album=self, photo=photo).first()
        if pa and isinstance(ordering, int) and 0 < ordering:
            pa.ordering = ordering
            pa.save()
            return True
        return False

    def save(self, *args, **kwargs):
        strip_text_items = ["title", "description"]
        for item in strip_text_items:
            setattr(self, item, strip_tags(getattr(self, item, None)))
        self.title = self.title[:99]

        if not self.friendly_token:
            while True:
                friendly_token = helpers.produce_friendly_token()
                if not PhotoAlbum.objects.filter(friendly_token=friendly_token):
                    self.friendly_token = friendly_token
                    break
        super(PhotoAlbum, self).save(*args, **kwargs)

    @property
    def thumbnail_url(self):
        pai = self.photoalbumitem_set.first()
        if pai and pai.photo.thumbnail:
            return helpers.url_from_path(pai.photo.thumbnail.path)
        return None


class PhotoAlbumItem(models.Model):
    """Helper model to store playlist specific media"""

    action_date = models.DateTimeField(auto_now=True)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    photo_album = models.ForeignKey(PhotoAlbum, on_delete=models.CASCADE)
    ordering = models.IntegerField(default=1)

    class Meta:
        ordering = ["ordering", "-action_date"]


from django.db import models
from posts.helpers import original_media_file_path, original_thumbnail_file_path

# from mptt.models import MPTTModel, TreeForeignKey
# # from media.services import Media
#
class Video(models.Model):
    s3_key       = models.CharField(max_length=400, null=True, blank=True)
    filename     = models.CharField(max_length=400, null=True, blank=True)

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    video_file = models.FileField(upload_to='media_files/videos/')

    sprites = models.FileField(upload_to=original_thumbnail_file_path, blank=True, max_length=500)
    thumbnail = models.FileField(upload_to=original_thumbnail_file_path, blank=True, max_length=500)

    # song = models.ForeignKey(Song, on_delete=models.CASCADE, blank=True)
    # user = models.ForeignKey('users.User', on_delete=models.CASCADE, blank=True)


class VideoPlaylist(models.Model):
    title = models.CharField(max_length=900, null=True, blank=True)
    videos = models.ManyToManyField(Video, through='VideoPlaylistItem')

class VideoPlaylistItem(models.Model):

    # media = models.ForeignKey(Media, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    playlist = models.ForeignKey(VideoPlaylist, on_delete=models.CASCADE)
    ordering = models.IntegerField(default=1)
