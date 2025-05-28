from django.db import models


class Channel(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE)

class ChannelPost(models.Model):
    channel    = models.ForeignKey(Channel, related_name='channelposts', on_delete=models.CASCADE)
    author     = models.ForeignKey('users.User', on_delete=models.CASCADE)  # user who authored this post in the channel
    content    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # for reposts
    original_post = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='reposts',
        on_delete=models.SET_NULL
    )

    class Meta:
        unique_together = ('channel', 'post')

class ChannelPostLike(models.Model):
    channelpost = models.ForeignKey(ChannelPost, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('channel_post', 'user')  # prevent duplicate likes
