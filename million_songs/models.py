# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class CdSeries(models.Model):
    name = models.CharField(unique=True, max_length=100)

    class Meta:
        db_table = 'cd_series'
        ordering = ['id']

    def __str__(self):
        return self.name


class Cds(models.Model):
    series = models.ForeignKey(CdSeries, models.CASCADE)
    name = models.CharField(unique=True, max_length=100)
    release_date = models.DateField(default='0001-1-1')

    class Meta:
        db_table = 'cds'
        ordering = ['id']

    def __str__(self):
        return self.name


class Characters(models.Model):
    name = models.CharField(unique=True, max_length=100)
    element = models.ForeignKey('Elements', models.CASCADE)

    class Meta:
        db_table = 'characters'
        ordering = ['id']

    def __str__(self):
        return self.name


class Elements(models.Model):
    name = models.CharField(unique=True, max_length=100)

    class Meta:
        db_table = 'elements'
        ordering = ['id']

    def __str__(self):
        return self.name


class Songs(models.Model):
    cd = models.ForeignKey(Cds, models.CASCADE)
    unit = models.ForeignKey('Units', models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)

    class Meta:
        db_table = 'songs'
        ordering = ['id']

    def __str__(self):
        return self.title


class SongSingers(models.Model):
    song = models.ForeignKey(Songs, models.CASCADE)
    singer = models.ForeignKey(Characters, models.CASCADE)

    class Meta:
        db_table = 'song_singers'
        unique_together = (('song', 'singer'),)


class Units(models.Model):
    name = models.CharField(max_length=100, null=True)
    is_everyone = models.BooleanField(default=False)
    song = models.ForeignKey(Songs, models.CASCADE, null=True)

    class Meta:
        db_table = 'units'
        ordering = ['song', 'id']
        constraints = [models.CheckConstraint(check=models.Q(name__isnull=True) & models.Q(is_everyone=False) |
                                                    models.Q(song__isnull=True),
                                              name='name_or_song_null')]

    def __str__(self):
        return self.name if self.name is not None else Songs.objects.get(pk=self.song_id).title


class UnitMembers(models.Model):
    unit = models.ForeignKey(Units, models.CASCADE)
    member = models.ForeignKey(Characters, models.CASCADE)

    class Meta:
        db_table = 'unit_members'
        unique_together = (('unit', 'member'),)


class WholeIdView(models.Model):
    cd_series_id = models.IntegerField(blank=True, null=True)
    cd_series_name = models.CharField(max_length=100, blank=True, null=True)
    cd_id = models.IntegerField(blank=True, null=True)
    cd_name = models.CharField(max_length=100, blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
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
