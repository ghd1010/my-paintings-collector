from rest_framework import serializers
from main_app.models import Painting, Mood, ColorPalette

class PaintingSerializer(serializers.ModelSerializer):
    mood = serializers.PrimaryKeyRelatedField(
        many = True,
        queryset = Mood.objects.all(),
        allow_empty = True,
        required = False
    )
    
    class Meta:
        model = Painting
        fields = '__all__'

class ColorPaletteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorPalette
        fields = '__all__'