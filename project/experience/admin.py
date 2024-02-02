from django.contrib import admin
from . import models as experience_models

# Register your models here.
admin.site.register(experience_models.City)
admin.site.register(experience_models.Attraction)
