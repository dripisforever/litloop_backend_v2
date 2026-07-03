from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0006_photo_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='r2_key',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
    ]
