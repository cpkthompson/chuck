# Generated by Django 2.2.1 on 2019-06-20 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0004_ideuser_finished'),
    ]

    operations = [
        migrations.AddField(
            model_name='ideuser',
            name='url',
            field=models.URLField(blank=True, unique=True),
        ),
    ]
