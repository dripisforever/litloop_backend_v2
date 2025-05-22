from django.db import models
from users.models import User
from videos.models import Video
from photos.models import Photo
from tracks.models import Track

#=========== PUBLIC CONVERSATION ======== #
class GroupChat(models.Model):
    name        = models.SlugField(max_length=20)
    image_url   = models.CharField(blank=True)
    description = models.CharField(blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)


class GroupUser(models.Model):
    user  = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True )
    group = models.ForeignKey(GroupChat, on_delete=models.SET_NULL, null=True, blank=True)
    joined_at = models.DateTimeField(auto_now_add=True)


class GroupMessage(models.Model):
    group        = models.ForeignKey(GroupChat, on_delete=models.SET_NULL, related_name="groupmessages")
    user         = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    text         = models.TextField(blank=True)

    videos       = models.ManyToManyField(Video, through='GroupMessageVideo', related_name='video_group_messages', null=True, blank=True, )
    photos       = models.ManyToManyField(Photo, through='GroupMessagePhoto', related_name='photo_group_messages', null=True, blank=True, )
    tracks       = models.ManyToManyField(Track, through='GroupMessageTrack', related_name='track_group_messages', null=True, blank=True, )

    created_at   = models.DateTimeField(auto_now_add=True)


class GroupMessageVideo(models.Model):
    message = models.ForeignKey(GroupMessage, on_delete=models.SET_NULL, null=True, blank=True)
    video   = models.ForeignKey(Video, null=True, blank=True)


class GroupMessagePhoto(models.Model):
    message = models.ForeignKey(GroupMessage, on_delete=models.SET_NULL, null=True, blank=True)
    photo   = models.ForeignKey(Photo, null=True, blank=True)


class GroupMessageTrack(models.Model):
    message = models.ForeignKey(GroupMessage, on_delete=models.SET_NULL, null=True, blank=True)
    track   = models.ForeignKey(Track, null=True)



# class Invite(models.Model):
#     pass
