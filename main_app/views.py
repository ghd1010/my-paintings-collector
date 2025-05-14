from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from django.views.generic.edit import UpdateView, DeleteView
from .models import Painting, Mood
from django.urls import reverse_lazy
from .forms import ColorPaletteForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def signup(request):
    # 1 - when it recieves GET request: render the signup template
    # 2 - When it gets a POST request: create the user then log them in
    if request.method == 'POST':
        # Make a UserCreation form, and if it is valid save the user and log them in
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save our user to the DB
            user = form.save()
            # Log in our user
            login(request, user)
            return redirect('home') # The return keyword will stop the function running here
    form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def home(request):
    return render(request, 'home.html')

@login_required
def assoc_mood( _, painting_id, mood_id):
    # add the painting_id to the painting.mood 1.get the painting
    Painting.objects.get(id= painting_id).mood.add(mood_id) #grap the painting obj from db with whTEVER painting id in url path, mood obj for this painting - addd the mood id to it
    return redirect('painting_details', painting_id= painting_id) #name of url path `'painting_details'`

@login_required
def dessoc_mood( _, painting_id, mood_id):
    Painting.objects.get(id= painting_id).mood.remove(mood_id)
    return redirect('painting_details', painting_id= painting_id) 

# Create your views here.
class PaintingListView(LoginRequiredMixin, ListView):
    model = Painting
    template_name = 'paintings_list.html' #same name of the file of html
    context_object_name = 'paintings'
    
    def get_queryset(self):
        return Painting.objects.filter(user = self.request.user)

@login_required
def painting_detail_view(request, painting_id): #painting_id is whatever we put in the params in urls.py
    painting = Painting.objects.get(id=painting_id)
    palette_form = ColorPaletteForm()
    # all un-associated painting moods
    mood_painting_not_have = Mood.objects.exclude(id__in = painting.mood.all().values_list('id'))

    return render(request, 'painting_details.html', {
        # The context sends the data to the template
        'painting': painting,
        'palette_form': palette_form,
        'mood_painting_not_have': mood_painting_not_have
    })

def add_palette(request, painting_id):
    form = ColorPaletteForm(request.POST)
    # make a new paletee form object
    # put the painting ID on it
    # save the palette to the Database
    if form.is_valid(): #will return T, F
        new_palette = form.save(commit = False) # pretend that it saved in DB, but it will be actuall saved in the computer RAM as if it was in the DB
        new_palette.painting_id = painting_id
        new_palette.save()
    return redirect('painting_details', painting_id = painting_id)

class CreatePaintingView(CreateView):
    model = Painting
    fields = ['name', 'colors_type', 'year_created', 'style']
    template_name = 'painting_form.html' 
    success_url = reverse_lazy('paintings_list')

    def form_valid(self, form):
        # Assign the logged in user  to the form instance
        # form.instance is the painting we are creating
        # self.request.user is the currently logged in user
        form.instance.user = self.request.user 
        return super().form_valid(form)

class UpdatePainingView(UpdateView):
    model = Painting
    fields = ['name', 'colors_type', 'year_created', 'style']
    template_name = 'painting_form.html' 
    success_url = reverse_lazy('paintings_list')
    
class DeletePainingView(DeleteView):
    model = Painting
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('paintings_list')


