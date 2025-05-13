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
