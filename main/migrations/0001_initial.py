# Generated by Django 5.1 on 2024-10-21 04:34

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=25, unique=True)),
                ('password', models.BinaryField(editable=True)),
                ('name', models.CharField(max_length=200, null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('email_is_verified', models.BooleanField(default=False)),
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('no_of_tickets', models.IntegerField(default=0)),
                ('ticket_id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('warned_email', models.BooleanField(default=False)),
            ],
        ),
    ]
