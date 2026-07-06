from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0003_add_author_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='notes.page')),
            ],
            options={
                'ordering': ['name'],
                'unique_together': {('page', 'name')},
            },
        ),
    ]
