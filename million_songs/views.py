from django.shortcuts import render, redirect

from million_songs.entities import SingerExt, SongAll
from million_songs.forms import CharacterForm, CdSeriesForm, CdsForm, UnitForm, SongForm, SearchForm
from million_songs.models import Elements, Units, UnitMembers, Songs, WholeIdView, CdSongs


def index(request):
    elements = Elements.objects.all().order_by('id')
    return render(request, 'million_songs/index.html', {'elements': elements})


def register(request):
    params = {'character_form': None, 'cd_series_form': None, 'cds_form': None,
              'unit_form': None, 'song_form': None, 'message': None}
    if request.method == 'POST':
        if 'character_button' in request.POST:
            character_form = CharacterForm(request.POST)
            if character_form.is_valid():
                character_form.save()
                return redirect('register')
        if 'cd_series_button' in request.POST:
            cd_series_form = CdSeriesForm(request.POST)
            if cd_series_form.is_valid():
                cd_series_form.save()
                return redirect('register')
        if 'cds_button' in request.POST:
            cds_form = CdsForm(request.POST)
            if cds_form.is_valid():
                cds_form.save()
                return redirect('register')
        if 'unit_button' in request.POST:
            unit_form = UnitForm(request.POST)
            if unit_form.is_valid():
                cleaned_data = unit_form.cleaned_data
                unit = Units()
                unit.name = cleaned_data['name']
                unit.is_everyone = cleaned_data['is_everyone']
                unit.save()
                for member in cleaned_data['unit_members']:
                    unit_member = UnitMembers()
                    unit_member.unit_id = unit.id
                    unit_member.member_id = member
                    unit_member.save()
                return redirect('register')
        if 'song_button' in request.POST:
            song_form = SongForm(request.POST)
            if song_form.is_valid():
                cleaned_data = song_form.cleaned_data
                if cleaned_data['is_existing_song'] and cleaned_data['existing_song'] is None:
                    return set_field(params, request, '曲名を選んでください')
                if not cleaned_data['is_existing_song'] and cleaned_data['title'].strip() == '':
                    return set_field(params, request, '曲名を入力してください')
                cd_song = CdSongs()
                cd_song.cd_id = cleaned_data['cd'].id
                if cleaned_data['has_unit_name']:
                    if cleaned_data['unit'] is None:
                        return set_field(params, request, 'ユニットを選んでください')
                    cd_song.unit_id = cleaned_data['unit'].id
                else:
                    if len(cleaned_data['singers']) == 0:
                        return set_field(params, request, '1人以上の歌手を選んでください')
                    unit = Units()
                    unit.is_everyone = False
                    unit.save()
                    for singer in cleaned_data['singers']:
                        unit_member = UnitMembers()
                        unit_member.unit_id = unit.id
                        unit_member.member_id = singer
                        unit_member.save()
                    cd_song.unit_id = unit.id
                if cleaned_data['is_existing_song']:
                    cd_song.song_id = cleaned_data['existing_song'].id
                else:
                    song = Songs()
                    song.title = cleaned_data['title']
                    song.save()
                    cd_song.song_id = song.id
                cd_song.save()

                return redirect('register')
    params['character_form'] = CharacterForm()
    params['cd_series_form'] = CdSeriesForm()
    params['cds_form'] = CdsForm()
    params['unit_form'] = UnitForm()
    params['song_form'] = SongForm()
    return render(request, 'million_songs/register.html', params)


def set_field(params, request, message):
    params['message'] = message
    params['character_form'] = CharacterForm()
    params['cd_series_form'] = CdSeriesForm()
    params['cds_form'] = CdsForm()
    params['unit_form'] = UnitForm()
    params['song_form'] = SongForm()
    return render(request, 'million_songs/register.html', params)


def view(request):
    search_form = SearchForm(request.POST)
    whole = WholeIdView.objects.all()
    cleaned_data = None
    is_singer_search_and = False  # and検索
    is_singer_search_or = False  # or検索
    if request.method == 'POST' and search_form.is_valid():
        cleaned_data = search_form.cleaned_data
        if cleaned_data['cd'] is not None:
            whole = whole.filter(cd_id=cleaned_data['cd'].id)
        if cleaned_data['unit'] is not None:
            whole = whole.filter(unit_id=cleaned_data['unit'].id)
        if len(cleaned_data['singers']) != 0:
            if cleaned_data['is_or_search']:
                is_singer_search_or = True
            else:
                is_singer_search_and = True

    song_list = []
    song = None
    cd_id_old = 0
    song_id_old = 0
    unit_id_old = 0
    for data in whole:
        if data.cd_id != cd_id_old or data.song_id != song_id_old or data.unit_id != unit_id_old:
            song = SongAll(data.cd_series_id, data.cd_series_name, data.cd_id,
                           data.cd_name, data.release_date, data.cd_song_id, data.song_id, data.song_title,
                           data.unit_id, data.unit_name, data.is_everyone)
            song_list.append(song)
            cd_id_old = data.cd_id
            song_id_old = data.song_id
            unit_id_old = data.unit_id
        singer = SingerExt(data.singer_id, data.singer_name, data.element_id, data.element_name)
        song.singer_list.append(singer)

    if is_singer_search_or:
        for song in song_list:
            song.removed = True
            for singer in song.singer_list:
                if str(singer.id) in cleaned_data['singers']:
                    song.removed = False
                    break

    if is_singer_search_and:
        for song in song_list:
            for form_singer in cleaned_data['singers']:
                in_singer_list = False
                for singer in song.singer_list:
                    if str(singer.id) == form_singer:
                        in_singer_list = True
                if not in_singer_list:
                    song.removed = True
                    break

    return render(request, 'million_songs/view.html', {'song_list': song_list, 'search_form': search_form})
