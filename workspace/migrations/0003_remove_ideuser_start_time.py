# Generated by Django 2.2.1 on 2019-06-03 11:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0002_auto_20190603_1137'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ideuser',
            name='start_time',
        ),
    ]