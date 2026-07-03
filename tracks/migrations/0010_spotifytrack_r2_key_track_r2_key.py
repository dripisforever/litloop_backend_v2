from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0009_track_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='spotifytrack',
            name='r2_key',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AddField(
            model_name='track',
            name='r2_key',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
    ]
