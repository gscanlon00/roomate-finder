# Generated by Django 4.0.1 on 2022-03-01 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_site', '0002_offer_receiver_alter_offer_from_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='receiver_name',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='offer',
            name='sender_name',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
