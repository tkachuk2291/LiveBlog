# Generated by Django 5.0.3 on 2024-04-03 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0005_alter_post_picture_alter_user_avatar"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="picture",
            field=models.ImageField(
                blank=True,
                default="post_photo_default/post_default_images.jpeg",
                null=True,
                upload_to="",
            ),
        ),
    ]
