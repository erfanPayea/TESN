# Generated by Django 5.0 on 2024-02-04 13:29

import experience.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experience', '0009_remove_post_file_path_remove_review_file_path_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=experience.models.upload_to_posts),
        ),
        migrations.AlterField(
            model_name='review',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=experience.models.upload_to_posts),
        ),
    ]
