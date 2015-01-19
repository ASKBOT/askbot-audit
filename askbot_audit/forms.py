from django import forms

class ItemForm(forms.Form):
    item_id = forms.IntegerField()

class ItemsForm(forms.Form):
    tag_ids = forms.CharField(required=False)
    languages = forms.CharField(required=False)
    user_name = forms.CharField(required=False)
    period = forms.CharField(required=False)
    sort_method = forms.CharField(required=False)

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

    WIP 

