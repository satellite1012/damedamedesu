from django import forms

class SongForm(forms.Form):
    name = forms.CharField(label='Name', max_length=256)
    url = forms.URLField(max_length=200)
    
class GroupForm(forms.Form):
    name = forms.CharField(label='Name', max_length=256)
    password = forms.CharField(label='Password', max_length=256)
    
class RatingForm(forms.Form):
    rating = forms.IntegerField(label='Rating', min_value=1, required=False)
    rank = forms.IntegerField(label='Rank', min_value=1, required=False)
    comment = forms.CharField(label='Comment', max_length=2048,
        required=False)