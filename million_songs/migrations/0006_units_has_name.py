# Generated by Django 3.1.5 on 2021-01-17 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('million_songs', '0005_auto_20210117_1233'),
    ]

    operations = [
        migrations.AddField(
            model_name='units',
            name='has_name',
            field=models.BooleanField(default=True),
        ),
    ]
