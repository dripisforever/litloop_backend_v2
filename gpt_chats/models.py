from django.db import models
from users.models import User
from videos.models import Video
from photos.models import Photo
from tracks.models import Track


#=========== CHATBOT CONVERSATION ======== #
class GptChat(models.Model):
    title      = models.SlugField(max_length=20)
    user       = models.ForeignKey(User, related_name='group_chats', on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or f"Chat {self.pk}"


class GptMessage(models.Model):

    chat = models.ForeignKey(GPTChat, on_delete=models.SET_NULL, related_name="messages")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


    prompt       = models.TextField()
    created_at   = models.DateTimeField(auto_now_add=True)




# class Invite(models.Model):
#     pass
