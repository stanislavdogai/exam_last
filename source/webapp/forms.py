from django import forms

from webapp.models import Ad


class SearchForm(forms.Form):
    search = forms.CharField(max_length=30, required=False, label="Найти")

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        exclude = ('author', 'public_at', 'created_at', 'updated_at', 'status',)