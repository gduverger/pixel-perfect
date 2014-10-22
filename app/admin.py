from django.contrib import admin
from app import models as app_models

admin.site.register(app_models.Test)
