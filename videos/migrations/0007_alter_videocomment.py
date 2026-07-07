from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_initial'),
        ('videos', '0006_videocomment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videocomment',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='videocomment',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='videocomment',
            name='text',
        ),
        migrations.RemoveField(
            model_name='videocomment',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='videocomment',
            name='user',
        ),
        migrations.AddField(
            model_name='videocomment',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_links', to='comments.Comment'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='videocomment',
            name='video',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_links', to='videos.video'),
        ),
        migrations.AddField(
            model_name='comment',
            name='videos',
            field=models.ManyToManyField(blank=True, related_name='comments', through='videos.VideoComment', to='videos.video'),
        ),
    ]
