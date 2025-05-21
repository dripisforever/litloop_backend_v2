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


class GroupMessage(models.Model):
    group        = models.ForeignKey(GrouChat, on_delete=models.CASCADE, related_name="messages")
    user         = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    text         = models.TextField(blank=True)

    videos       = models.ManyToManyField(Video, through='MessageVideo', related_name='video_group_messages', null=True, blank=True, on_delete=models.SET_NULL)
    photos       = models.ManyToManyField(Photo, through='MessagePhoto', related_name='photo_group_messages', null=True, blank=True, on_delete=models.SET_NULL)
    tracks       = models.ManyToManyField(Track, through='MessageTrack', related_name='travk_group_messages', null=True, blank=True, on_delete=models.SET_NULL)
    attachments  = models.ManyToManyField(Attachment, blank=True)

    created_at   = models.DateTimeField(default=timezone.localtime().now)


class GroupUser(models.Model):
    user  = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True )
    group = models.ForeignKey(GroupChat, on_delete=models.SET_NULL, null=True, blank=True)



#=========== USER CONVERSATION ======== #
class Chat(models.Model):
    name        = models.SlugField(max_length=20)
    image_url   = models.CharField(blank=True)
    description = models.CharField(blank=True)


class Message(models.Model):
    chat         = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    user         = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    text         = models.TextField(blank=True)
    videos       = models.ManyToManyField(Video, through='MessageVideo', related_name='video_messages', null=True, blank=True, on_delete=models.SET_NULL)
    photos       = models.ManyToManyField(Photo, through='MessagePhoto', related_name='photo_messages', null=True, blank=True, on_delete=models.SET_NULL)
    tracks       = models.ManyToManyField(Track, through='MessageTrack', related_name='track_messages',null=True, blank=True, on_delete=models.SET_NULL)

    created_at   = models.DateTimeField(default=timezone.localtime().now)


class MessageVideo(models.Model):
    message = models.ForeignKey(Message, on_delete=models.SET_NULL, null=True, blank=True)
    video   = models.ForeignKey(Video, on_delete=models.CASCADE)


class MessagePhoto(models.Model):
    message = models.ForeignKey(Message, on_delete=models.SET_NULL, null=True, blank=True)
    photo   = models.ForeignKey(Photo, on_delete=models.SET_NULL, null=True, blank=True)


class MessageTrack(models.Model):
    message = models.ForeignKey(Message, on_delete=models.SET_NULL, null=True, blank=True)
    track   = models.ForeignKey(Track, on_delete=models.CASCADE)



#=========== CHATBOT CONVERSATION ======== #
class GPTChat(models.Model):
    title      = models.SlugField(max_length=20)
    user       = models.ForeignKey(User, related_name='group_chats')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or f"Chat {self.pk}"


class GPTMessage(models.Model):

    chat = models.ForeignKey(GPTChat, on_delete=models.CASCADE, related_name="messages")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


    prompt       = models.TextField()
    created_at   = models.DateTimeField(default=timezone.localtime().now)




# class Invite(models.Model):
#     pass
