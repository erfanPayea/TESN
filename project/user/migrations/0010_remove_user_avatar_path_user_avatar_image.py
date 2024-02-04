# Generated by Django 5.0 on 2024-02-04 13:29

import user.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_alter_user_avatar_path'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='avatar_path',
        ),
        migrations.AddField(
            model_name='user',
            name='avatar_image',
            field=models.ImageField(blank=True, null=True, upload_to=user.models.upload_to),
        ),
    ]