# Generated by Django 3.1.5 on 2021-01-17 05:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('million_songs', '0006_units_has_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='units',
            options={'ordering': ['has_name', 'id']},
        ),
    ]