# Generated by Django 4.0.1 on 2022-03-03 01:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_site', '0005_offer_property_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
    ]
