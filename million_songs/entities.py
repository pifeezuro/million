from million_songs.models import CdSeries, Cds, Songs, Characters


class CdSeriesExt(CdSeries):
    def __init__(self, cd_series_id, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = cd_series_id
        self.name = name
        self.cd_list = []


class CdExt(Cds):
    def __init__(self, cd_id, series_id, name, release_date, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = cd_id
        self.series_id = series_id
        self.name = name
        self.release_date = release_date
        self.song_list = []


class SongExt(Songs):
    def __init__(self, song_id, cd_id, title, unit_id, unit_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = song_id
        self.cd_id = cd_id
        self.title = title
        self.unit_id = unit_id
        self.unit_name = unit_name
        self.singer_list = []


class SongAll:
    def __init__(self, cd_series_id, cd_series_name, cd_id, cd_name, release_date,
                 cd_song_id, song_id, song_title, unit_id, unit_name, is_everyone):
        self.cd_series_id = cd_series_id
        self.cd_series_name = cd_series_name
        self.cd_id = cd_id
        self.cd_name = cd_name
        self.release_date = release_date
        self.cd_song_id = cd_song_id
        self.song_id = song_id
        self.song_title = song_title
        self.unit_id = unit_id
        self.unit_name = unit_name
        self.is_everyone = is_everyone
        self.singer_list = []
        self.removed = False


class SingerExt(Characters):
    def __init__(self, singer_id, name, element_id, element_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = singer_id
        self.name = name
        self.element_id = element_id
        self.element_name = element_name
