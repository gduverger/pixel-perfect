from django.db import models


class Test(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    file = models.FileField(upload_to='mocks')
    link = models.URLField(max_length=500)

