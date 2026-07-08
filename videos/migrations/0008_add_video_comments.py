from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0007_alter_videocomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='comments',
            field=models.ManyToManyField(blank=True, related_name='videos', through='videos.VideoComment', to='comments.Comment'),
        ),
    ]
