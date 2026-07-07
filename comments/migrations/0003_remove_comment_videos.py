from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='videos',
        ),
    ]
