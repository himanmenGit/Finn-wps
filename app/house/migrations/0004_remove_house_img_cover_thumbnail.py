# Generated by Django 2.0.3 on 2018-04-15 11:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0003_house_img_cover_thumbnail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='house',
            name='img_cover_thumbnail',
        ),
    ]