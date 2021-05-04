import copy

from django.shortcuts import render, redirect

from million_songs.entities import CdSeriesExt, CdExt, SongExt, SingerExt
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

    cd_series_list = []
    form_singers = []  # 検索フォームに入力されたキャラのリストのコピー and検索に使う
    is_added = False  # その曲がリストに追加されたか
    cd_series = None
    cd = None
    song = None
    cd_series_id_old = 0
    cd_id_old = 0
    song_id_old = 0
    unit_id_old = 0
    for data in whole:  # CDシリーズ->CD->楽曲->歌手の形でオブジェクトに入れていく
        if data.cd_series_id != cd_series_id_old:
            cd_series = CdSeriesExt(data.cd_series_id, data.cd_series_name)
            cd_series_list.append(cd_series)
            cd_series_id_old = data.cd_series_id
        if data.cd_id != cd_id_old:
            cd = CdExt(data.cd_id, data.cd_series_id, data.cd_name, data.release_date)
            cd_series.cd_list.append(cd)
            cd_id_old = data.cd_id
            song_id_old = 0
            unit_id_old = 0
        if data.song_id != song_id_old or data.unit_id != unit_id_old:
            is_added = False
            if is_singer_search_and:
                form_singers = copy.deepcopy(cleaned_data['singers'])
                # formのsingersをディープコピー
            song = SongExt(data.song_id, data.cd_id, data.song_title, data.unit_id, data.unit_name)
            if not is_singer_search_or and not is_singer_search_and:  # 歌手指定がない場合無条件でリストに追加
                cd.song_list.append(song)
            song_id_old = data.song_id
            unit_id_old = data.unit_id
        singer = SingerExt(data.singer_id, data.singer_name, data.element_id, data.element_name)
        song.singer_list.append(singer)
        if is_singer_search_or and str(singer.id) in cleaned_data['singers'] and not is_added:
            # or検索の場合、曲の歌手とsingersリストに共通があれば条件を満たす曲としてリストに追加
            cd.song_list.append(song)
            is_added = True
        if is_singer_search_and and str(singer.id) in form_singers:
            # and検索の場合、曲のsingerがform_singersリストにあるとそのキャラをform_singersから削除
            form_singers.remove(str(singer.id))
        if is_singer_search_and:
            # form_singersが空(リスト内の全キャラが曲のsingersに含まれている)の場合、条件を満たす曲としてリストに追加
            if len(form_singers) == 0 and not is_added:
                cd.song_list.append(song)
                is_added = True

    return render(request, 'million_songs/view.html', {'cd_series_list': cd_series_list, 'search_form': search_form})
