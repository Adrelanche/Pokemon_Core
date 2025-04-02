from django.urls import path
from .views import (
    RegisterUserView,
    FavoritePokemonToggleView,
    LoginView,
    FavoritePokemonOrder,
)

urlpatterns = [
    path('api/register/', RegisterUserView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/favorite/', FavoritePokemonToggleView.as_view(), name='favorite'),
    path('api/favorite-order/', FavoritePokemonOrder.as_view(), name='favorite-order'),
]
