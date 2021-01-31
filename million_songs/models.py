# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class CdSeries(models.Model):
    name = models.CharField(unique=True, max_length=100)

    class Meta:
        db_table = 'cd_series'

    def __str__(self):
        return self.name


class CdSongs(models.Model):
    cd = models.ForeignKey('Cds', models.DO_NOTHING, blank=True, null=True)
    song = models.ForeignKey('Songs', models.DO_NOTHING, blank=True, null=True)
    unit = models.ForeignKey('Units', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'cd_songs'


class Cds(models.Model):
    name = models.CharField(unique=True, max_length=100)
    series = models.ForeignKey(CdSeries, models.DO_NOTHING)
    release_date = models.DateField()

    class Meta:
        db_table = 'cds'

    def __str__(self):
        return self.name


class Characters(models.Model):
    name = models.CharField(unique=True, max_length=100)
    element = models.ForeignKey('Elements', models.DO_NOTHING)

    class Meta:
        db_table = 'characters'

    def __str__(self):
        return self.name


class Elements(models.Model):
    name = models.CharField(unique=True, max_length=100)

    class Meta:
        db_table = 'elements'

    def __str__(self):
        return self.name


class Songs(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        db_table = 'songs'

    def __str__(self):
        return self.title


class UnitMembers(models.Model):
    member = models.ForeignKey(Characters, models.DO_NOTHING)
    unit = models.ForeignKey('Units', models.DO_NOTHING)

    class Meta:
        db_table = 'unit_members'
        unique_together = (('unit', 'member'),)


class Units(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    is_everyone = models.BooleanField()

    class Meta:
        db_table = 'units'

    def __str__(self):
        return self.name


class WholeIdView(models.Model):
    cd_series_id = models.IntegerField(blank=True, null=True)
    cd_series_name = models.CharField(max_length=100, blank=True, null=True)
    cd_id = models.IntegerField(blank=True, null=True)
    cd_name = models.CharField(max_length=100, blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    cd_song_id = models.IntegerField(blank=True, null=True)
    song_id = models.IntegerField(blank=True, null=True)
    song_title = models.CharField(max_length=100, blank=True, null=True)
    unit_id = models.IntegerField(blank=True, null=True)
    unit_name = models.CharField(max_length=100, blank=True, null=True)
    is_everyone = models.BooleanField(blank=True, null=True)
    unit_member_id = models.IntegerField(blank=True, null=True)
    singer_id = models.IntegerField(blank=True, null=True)
    singer_name = models.CharField(max_length=100, blank=True, null=True)
    element_id = models.IntegerField(blank=True, null=True)
    element_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'whole_id_view'
