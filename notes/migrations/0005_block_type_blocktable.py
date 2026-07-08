from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0004_pagetag'),
    ]

    operations = [
        migrations.AddField(
            model_name='block',
            name='type',
            field=models.CharField(choices=[('text', 'Text'), ('table', 'Table')], default='text', max_length=20),
        ),
        migrations.CreateModel(
            name='BlockTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('columns', models.JSONField(default=list)),
                ('rows', models.JSONField(default=list)),
                ('block', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='table_data', to='notes.block')),
            ],
        ),
    ]
