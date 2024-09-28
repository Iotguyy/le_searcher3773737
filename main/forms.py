from django import forms
from .models import NameRecord

class NameRecordForm(forms.ModelForm):
    class Meta:
        model = NameRecord
        fields = ['first_name', 'last_name']




class NameSearchForm(forms.Form):
    SEARCH_TYPES = [
        ('exact', 'Exact Match'),
        ('fuzzy', 'Fuzzy Search'),
        ('phonetic', 'Phonetic Search'),
    ]
    query = forms.CharField(max_length=200, required=True, label="Search Name")
    search_type = forms.ChoiceField(choices=SEARCH_TYPES, required=True, initial='exact')