from django.contrib import admin
from .models import Pokemon, Evolution, Trainer, Photo

# Register your models here.
admin.site.register(Pokemon)
admin.site.register(Evolution)
admin.site.register(Trainer)
admin.site.register(Photo)
