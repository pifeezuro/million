# Generated by Django 3.1.5 on 2021-01-18 13:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('million_songs', '0014_auto_20210117_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cds',
            name='series',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='million_songs.cdseries'),
        ),
        migrations.AlterField(
            model_name='characters',
            name='element',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='million_songs.elements'),
        ),
        migrations.AlterField(
            model_name='songs',
            name='cd',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='million_songs.cds'),
        ),
        migrations.AlterField(
            model_name='songsingers',
            name='singer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='million_songs.characters'),
        ),
        migrations.AlterField(
            model_name='songsingers',
            name='song',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='million_songs.songs'),
        ),
        migrations.AlterField(
            model_name='unitmembers',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='million_songs.characters'),
        ),
        migrations.AlterField(
            model_name='unitmembers',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='million_songs.units'),
        ),
    ]
