# Generated by Django 2.0.3 on 2018-04-03 02:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0004_auto_20180403_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='signup_type',
            field=models.CharField(blank=True, choices=[('f', 'facebook'), ('e', 'email')], default='e', max_length=1),
        ),
    ]