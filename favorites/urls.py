from django.urls import path

from .views import favorites_list, add_to_favorites, remove_from_favorites, delete_favorites

urlpatterns = [
    path('', favorites_list, name='favorites_list'),
    path('<id>/add/', add_to_favorites, name='add_to_favorites'),
    path('<id>/remove/', remove_from_favorites, name='remove_from_favorites'),
    path('delete/', delete_favorites, name='delete_favorites'),
]
