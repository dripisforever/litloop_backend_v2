from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0009_voicemessage_transcribed_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='voicemessage',
            name='r2_key',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
    ]
