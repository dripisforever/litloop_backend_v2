from django.db import models
from django.conf import settings
from mptt.models import MPTTModel, TreeForeignKey

class Page(MPTTModel):
    title = models.CharField(max_length=200)
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        on_delete=models.CASCADE
    )
    is_locked  = models.BooleanField(default=False)
    is_private = models.BooleanField(default=True)
    author     = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='pages', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['title']

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'parent_id': self.parent_id,
            'tags': [t.name for t in self.tags.all()],
            'tag_ids': [t.id for t in self.tags.all()],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }

class PageTag(models.Model):
    page = models.ForeignKey(Page, related_name='tags', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('page', 'name')
        ordering = ['name']

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'page_id': self.page_id,
        }

class Block(models.Model):
    page = models.ForeignKey(Page, related_name='blocks', on_delete=models.CASCADE)
    content = models.TextField(default='', blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'order': self.order,
            'page_id': self.page_id,
        }
