from django import forms
from django.conf import settings as django_settings

def str_to_int(val):
    try:
        return int(val.strip())
    except (TypeError, ValueError):
        return None

class ItemForm(forms.Form):
    item_id = forms.IntegerField()

class ItemsForm(forms.Form):
    tag_ids = forms.CharField(required=False)
    languages = forms.CharField(required=False)
    user_name = forms.CharField(required=False)
    period = forms.CharField(required=False)
    sort_method = forms.CharField(required=False)

    def clean_tag_ids(self):
        tag_ids = self.cleaned_data.get('tag_ids', '')
        tag_ids = tag_ids.split(',')
        tag_ids = map(str_to_int, tag_ids)
        tag_ids = list(set(tag_ids))
        tag_ids.remove(None)
        self.cleaned_data['tag_ids'] = tag_ids
        return tag_ids

    def clean_period(self):
        period = self.cleaned_data.get('period', 'any')
        if period not in ('any', 'day', 'week', 'month'):
            period = 'any'
        self.cleaned_data['period'] = period
        self.cleaned_data['period']

    def clean_languages(self):
        languages = self.cleaned_data.get('languages', '')
        languages = set(languages.split(','))
        available_langs = set(dict(django_settings.LANGUAGES).keys())
        languages &= available_langs
        self.cleaned_data['languages'] = list(languages)
        return self.cleaned_data['languages']

    def clean_user_name(self):
        user_name = self.cleaned_data.get('user_name', '').strip()

    def clean_sort_method(self):
        sort_method = self.cleaned_data.get('sort_method', 'date').strip()
        if sort_method not in ('date', 'activity', 'answers', 'votes'):
            sort_method = 'date'

