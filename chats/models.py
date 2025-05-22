from django.db import models
from users.models import User
from videos.models import Video
from photos.models import Photo
from tracks.models import Track


class Chat(models.Model):
    name        = models.SlugField(max_length=20)
    image_url   = models.CharField(blank=True)
    description = models.CharField(blank=True)


class Message(models.Model):
    chat         = models.ForeignKey(Chat, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages")
    user         = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    text         = models.TextField(blank=True)
    videos       = models.ManyToManyField(Video, through='MessageVideo', related_name='video_messages', blank=True, )
    photos       = models.ManyToManyField(Photo, through='MessagePhoto', related_name='photo_messages', blank=True, )
    tracks       = models.ManyToManyField(Track, through='MessageTrack', related_name='track_messages', blank=True, )

    created_at   = models.DateTimeField(auto_now_add=True)


class MessageVideo(models.Model):
    message = models.ForeignKey(Message, on_delete=models.SET_NULL, null=True, blank=True)
    video   = models.ForeignKey(Video, on_delete=models.SET_NULL, null=True, blank=True)


class MessagePhoto(models.Model):
    message = models.ForeignKey(Message, on_delete=models.SET_NULL, null=True, blank=True)
    photo   = models.ForeignKey(Photo, on_delete=models.SET_NULL, null=True, blank=True)


class MessageTrack(models.Model):
    message = models.ForeignKey(Message, on_delete=models.SET_NULL, null=True, blank=True)
    track   = models.ForeignKey(Track, on_delete=models.SET_NULL, null=True, blank=True)


# class Invite(models.Model):
#     pass
