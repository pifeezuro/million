from datetime import date

from django import forms

from million_songs.models import Characters, CdSeries, Cds, Units, Songs


class CharacterForm(forms.ModelForm):
    class Meta:
        model = Characters
        fields = '__all__'
        labels = {
            'name': '名前',
            'element': '属性'
        }


class CdSeriesForm(forms.ModelForm):
    class Meta:
        model = CdSeries
        fields = '__all__'
        labels = {
            'name': '名前'
        }


class CdsForm(forms.ModelForm):
    class Meta:
        model = Cds
        fields = '__all__'
        labels = {
            'series': 'CDシリーズ',
            'name': '名前',
            'release_date': '発売日'
        }
        widgets = {
            'release_date': forms.SelectDateWidget(years=[x for x in range(2013, date.today().year)])
        }


class UnitForm(forms.Form):
    name = forms.CharField(label='ユニット名', max_length=100, required=True)
    is_everyone = forms.BooleanField(label='全体ユニット', required=False)
    unit_members = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, required=True,
                                             choices=lambda: [(character.id, character.name)
                                                              for character in Characters.objects.all()],
                                             label='ユニットメンバー')


class SongForm(forms.Form):
    cd = forms.ModelChoiceField(label='CD名', required=True, queryset=Cds.objects.all())
    is_existing_song = forms.BooleanField(label='既存曲を登録', required=False)
    title = forms.CharField(label='タイトル', max_length=100, required=False)
    existing_song = forms.ModelChoiceField(label='タイトル', required=False, queryset=Songs.objects.all())
    has_unit_name = forms.BooleanField(label='ユニット名あり', required=False)
    unit = forms.ModelChoiceField(label='ユニット名', required=False, queryset=Units.objects.filter(name__isnull=False))
    singers = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, required=False,
                                        choices=lambda: [(character.id, character.name)
                                                         for character in Characters.objects.all()],
                                        label='歌手')
