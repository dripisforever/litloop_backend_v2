import uuid
# import media.helpers as helpers
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

class Comment(MPTTModel):
    add_date       = models.DateTimeField(auto_now_add=True)
    friendly_token = models.CharField(blank=True, max_length=27, db_index=True)
    text           = models.TextField(help_text="text")
    uid            = models.UUIDField(unique=True, default=uuid.uuid4)
    user           = models.ForeignKey("users.User", on_delete=models.CASCADE, db_index=True)
    parent         = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")

    # photos = models.ManyToManyField(User, through="CommentPhoto", related_name="comment_photos")
    # videos = models.ManyToManyField(User, through="CommentVideo", related_name="comment_videos")
    # tracks = models.ManyToManyField(User, through="CommentTrack", related_name="comment_tracks")

    # user = models.ForeignKey('users.User', related_name='comments', on_delete=models.CASCADE)

    class MPTTMeta:
        order_insertion_by = ["add_date"]

 
    def save(self, *args, **kwargs):
        strip_text_items = ["text"]
        for item in strip_text_items:
            setattr(self, item, strip_tags(getattr(self, item, None)))
        if self.text:
            self.text = self.text[: settings.MAX_CHARS_FOR_COMMENT]
        if not self.friendly_token:
            while True:
                friendly_token = helpers.produce_friendly_token(26)
                if not Comment.objects.filter(friendly_token=friendly_token):
                    self.friendly_token = friendly_token
                    break
        super(Comment, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("get_media") + "?m={0}".format(self.media.friendly_token)

    @property
    def media_url(self):
        return self.get_absolute_url()



class CommentPhoto(models.Model):
    pass

class CommentVideo(models.Model):
    pass

class CommentAudio(models.Model):
    pass

class CommentTrack(models.Model):
    pass
