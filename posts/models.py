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
