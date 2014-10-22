from django.forms import ModelForm

from app import models as app_models

class Test(ModelForm):
    class Meta:
        model = app_models.Test
        fields = ['name', 'file', 'link']
