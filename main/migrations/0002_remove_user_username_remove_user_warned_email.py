# Generated by Django 5.1 on 2024-10-21 04:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
        migrations.RemoveField(
            model_name='user',
            name='warned_email',
        ),
    ]