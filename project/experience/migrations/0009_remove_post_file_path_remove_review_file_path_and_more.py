# Generated by Django 5.0 on 2024-02-04 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experience', '0008_alter_attraction_path_alter_post_file_path_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='file_path',
        ),
        migrations.RemoveField(
            model_name='review',
            name='file_path',
        ),
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='review',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
