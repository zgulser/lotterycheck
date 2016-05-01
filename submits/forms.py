from django.forms import ModelForm
from django import forms
from submits import models

class LotteryPlayerForm(ModelForm):
    class Meta:
        model = models.LotteryPlayer
        fields = ['firstname', 'lastname', 'identity']

    def __init__(self, *args, **kwargs):
        super(LotteryPlayerForm, self).__init__(*args, **kwargs)

class ConfirmationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ConfirmationForm, self).__init__(*args, **kwargs)

class ExistsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ExistsForm, self).__init__(*args, **kwargs)
