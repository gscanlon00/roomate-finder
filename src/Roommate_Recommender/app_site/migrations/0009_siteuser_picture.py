# Generated by Django 4.0.1 on 2022-03-03 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_site', '0008_delete_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteuser',
            name='picture',
            field=models.FileField(default='user_img/default_pic.png', upload_to='user_img'),
        ),
    ]
