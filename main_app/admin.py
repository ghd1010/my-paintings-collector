from django.contrib import admin
from .models import Painting, ColorPalette, Mood

# Register your models here.
admin.site.register(Painting)
admin.site.register(ColorPalette)
admin.site.register(Mood)

