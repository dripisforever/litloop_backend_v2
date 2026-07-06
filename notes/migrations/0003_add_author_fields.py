from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_username'),
        ('notes', '0002_page_is_locked_page_is_private'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pages', to='users.user'),
        ),
        migrations.AddField(
            model_name='page',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default='2025-01-01 00:00:00'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='page',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='block',
            name='content',
            field=models.TextField(blank=True, default=''),
        ),
    ]
