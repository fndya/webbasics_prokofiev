from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),  # главная, у тебя уже есть
    path("albums/", views.album_list, name="album_list"),
    path("albums/add/", views.album_create, name="album_create"),
    path("albums/<int:album_id>/", views.album_detail, name="album_detail"),
    path("albums/<int:album_id>/edit/", views.album_update, name="album_update"),
    path("albums/<int:album_id>/delete/", views.album_delete, name="album_delete"),
    path("favorite/<int:album_id>/", views.toggle_favorite, name="toggle_favorite"),
]