from django import forms as django_forms

from app import models as app_models

class Test(django_forms.ModelForm):
    class Meta:
        model = app_models.Test
        fields = ['name', 'file', 'link']
        widgets = {
            'link': django_forms.TextInput(attrs={'value': 'http://www.ebay.com/today'}),
        }
