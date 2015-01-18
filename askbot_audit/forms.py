from django import forms

class ItemForm(forms.Form):
    item_id = forms.IntegerField()
