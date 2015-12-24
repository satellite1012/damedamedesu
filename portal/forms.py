from django import forms
from decimal import Decimal

class SongForm(forms.Form):
    name = forms.CharField(label='Name', max_length=256)
    url = forms.URLField(label='Url', max_length=200)
    
class AddSongForm(forms.Form):
    name = forms.CharField(label='Name', max_length=256)
    url = forms.URLField(label='Url', max_length=200)
    
    def __init__(self, *args, **kwargs):
        mlist = kwargs.pop('mlist')
        super(AddSongForm, self).__init__(*args, **kwargs)
        self.fields['suggested_members'] = forms.ModelMultipleChoiceField(label='Suggested', queryset=mlist)
    
class GroupForm(forms.Form):
    name = forms.CharField(label='Name', max_length=256)
    password = forms.CharField(label='Password', max_length=256)
    
class RatingForm(forms.Form):
    rating = forms.IntegerField(label='Rating', min_value=Decimal(1),
        max_value=Decimal(10), required=False)
    rank = forms.IntegerField(label='Rank', min_value=1, required=False)
    comment = forms.CharField(label='Comment', max_length=2048,
        required=False)
        
        