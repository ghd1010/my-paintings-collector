from django.urls import path
from .views import (
    PaintingListView, 
    CreatePaintingView, 
    UpdatePainingView, 
    DeletePainingView,
    painting_detail_view,
    add_palette,
    assoc_mood,
    dessoc_mood,
    home,
    signup
    )

urlpatterns = [
    path('', home, name='home'),
    path('home/', home, name='home'),
    path('all-paintings/', PaintingListView.as_view(), name = 'paintings_list'),
    path('all-paintings/<int:painting_id>/', painting_detail_view, name= 'painting_details'),
    path('all-paintings/add', CreatePaintingView.as_view(), name= 'painting_create'),
    path('all-paintings/<int:pk>/update/', UpdatePainingView.as_view(), name='painting_update'),
    path('all-paintings/<int:pk>/delete', DeletePainingView.as_view(), name='painting_delete'),
    path('all-paintings/<int:painting_id>/add-palette', add_palette, name='add_palette'),
    path('all-paintings/<int:painting_id>/assoc-mood/<int:mood_id>', assoc_mood, name='assoc_mood'),
    path('all-paintings/<int:painting_id>/dessoc-mood/<int:mood_id>', dessoc_mood, name='dessoc_mood'),
    path('accounts/signup', signup, name='signup')
]
