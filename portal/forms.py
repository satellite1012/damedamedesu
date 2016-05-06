from django import forms
import datetime

class AddGame(forms.Form):
    day = forms.DateField(initial=datetime.date.today)
    champ1 = forms.CharField(label='Champion 1', max_length=128, required=True)
    champ2 = forms.CharField(label='Champion 2', max_length=128, required=True)
    champ3 = forms.CharField(label='Champion 3', max_length=128, required=True)
    champ4 = forms.CharField(label='Champion 4', max_length=128, required=True)
    champ5 = forms.CharField(label='Champion 5', max_length=128, required=True)
    