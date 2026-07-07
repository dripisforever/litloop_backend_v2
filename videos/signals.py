from django.db.models.signals import post_save
from django.dispatch import receiver
from videos.models import Video, VideoComment
from comments.models import Comment


FAKE_COMMENTS = [
    "Nice video! 🔥",
    "Great content, keep it up!",
    "Thanks for sharing this!",
]


@receiver(post_save, sender=Video)
def seed_fake_comments(sender, instance, created, **kwargs):
    if not created:
        return

    author = instance.user
    if not author:
        return

    for text in FAKE_COMMENTS:
        comment = Comment.objects.create(
            user=author,
            text=text,
        )
        VideoComment.objects.create(
            comment=comment,
            video=instance,
        )
