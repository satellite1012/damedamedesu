from django import forms

class SongForm(forms.Form):
    name = forms.CharField(label='Name', max_length=256)
    url = forms.URLField(max_length=200)
    
class GroupForm(forms.Form):
    name = forms.CharField(label='Name', max_length=256)
    password = forms.CharField(label='Password', max_length=256)
    
