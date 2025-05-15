# https://chatgpt.com/c/670e8061-9950-800c-aeb9-3145843f0b85
from django.db import models
from users.models import User
from videos.models import Video
from photos.models import Photo
from tracks.models import Track
#
#
class GroupChat(models.Model):
    name = models.SlugField(max_length=20)
    description = models.CharField(blank=True)
    members = models.ManyToManyField(User, related_name='group_chats')
    # messages = models.ManyToManyField(Message, blank=True )

class MessageTrack(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)
    comment = models.TextField(blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('message', 'track')
        ordering = ['order']

class Message(models.Model):
    parent_group = models.ForeignKey(GroupChat, on_delete=models.CASCADE, related_name="messages")
    # parent_user = models.ForeignKey(User, on_delete=models.SET(get_sentinal_user))
    parent_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    # groupchat = models.ForeignKey(GroupChat, on_delete=models.CASCADE, related_name='messages')
    # sender = models.ForeignKey(User, on_delete=models.CASCADE)
    # content = models.TextField(blank=True)

    message_text = models.TextField(blank=True)
    date_posted = models.DateTimeField(default=timezone.localtime().now)
    videos = models.ManyToManyField(Video, through='MessageVideo', related_name='messages', null=True, blank=True, on_delete=models.SET_NULL)
    photos = models.ManyToManyField(Photo, through='MessagePhoto', related_name='messages', null=True, blank=True, on_delete=models.SET_NULL)
    tracks = models.ManyToManyField(Track, through='MessageTrack', related_name='messages',null=True, blank=True, on_delete=models.SET_NULL)
    attachments = models.ManyToManyField(Attachment, blank=True)

    # track = models.ForeignKey(Track,  null=True, blank=True, on_delete=models.SET_NULL)

# class Attachment(models.Model):
#     file = models.FileField(upload_to='attachments/')
#
#
# class Invite(models.Model):
#     pass
