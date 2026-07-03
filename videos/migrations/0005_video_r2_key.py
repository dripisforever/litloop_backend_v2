from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0004_video_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='r2_key',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
    ]
