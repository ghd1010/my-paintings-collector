from django.urls import path
from .views import PaintingListAPI, CreatePaletteAPI, add_mood_to_painting, remove_mood_from_painting, SignUpView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('paintings/', PaintingListAPI.as_view(), name='api_paintings'),
    path('paintings/<int:painting_id>/add-palette', CreatePaletteAPI.as_view(), name='api_add_palette'),
    path('paintings/<int:painting_id>/add-mood/<int:mood_id>', add_mood_to_painting, name='api_add_mood_to_painting'),
    path('paintings/<int:painting_id>/remove-mood/<int:mood_id>', remove_mood_from_painting, name='api_remove_mood_from_painting'),
    
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', SignUpView.as_view(), name='signup')
]
