from django.db import models
from django.contrib.auth.models import User



# Create your models here.

class Mood(models.Model):
    feeling = models.CharField(max_length=50)

    def __str__(self):
        return self.feeling


class Painting(models.Model):
    name = models.CharField(max_length=100)
    # got from: https://www.geeksforgeeks.org/how-to-use-django-field-choices/
    COLORS_TYPE_LIST = [('Oil', 'Oil'),
                        ('Acrylics', 'Acrylics'),
                        ('Watercolor', 'Watercolor'),
                        ('Pencil', 'Pencil'),] 
    colors_type = models.CharField(
        max_length=20,
        choices=COLORS_TYPE_LIST, 
        default=COLORS_TYPE_LIST[0][0])
    year_created = models.PositiveIntegerField()
    style = models.CharField(max_length=100)
    mood = models.ManyToManyField(Mood)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.name} - {self.year_created}'
    
    
class ColorPalette(models.Model):
    name = models.CharField(max_length=100)
    colors = models.TextField()
    note = models.TextField(max_length=50)

    painting = models.ForeignKey(Painting, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.painting.name}'
    
    class Meta:
        ordering = ['name']


