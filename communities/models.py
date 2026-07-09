from django.db import models
from django.conf import settings


class Community(models.Model):
    name        = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon        = models.CharField(max_length=500, blank=True, null=True)
    banner      = models.CharField(max_length=500, blank=True, null=True)
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_communities')
    members     = models.ManyToManyField(settings.AUTH_USER_MODEL, through='CommunityMembership', related_name='communities')
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class CommunityMembership(models.Model):
    ROLE_CHOICES = [
        ('member', 'Member'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
    ]

    user      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    role      = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'community')


class CommunityPost(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    post         = models.OneToOneField('posts.Post', on_delete=models.CASCADE, related_name='community_post')
    community    = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='posts')
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='community_post_requests')
    status       = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reviewed_by  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='community_post_reviews')
    reviewed_at  = models.DateTimeField(null=True, blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
