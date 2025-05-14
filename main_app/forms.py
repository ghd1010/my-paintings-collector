from django.forms import ModelForm
from .models import ColorPalette

class ColorPaletteForm(ModelForm):
    class Meta:
        model = ColorPalette
        fields = ['name', 'colors', 'note']