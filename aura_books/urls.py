from django.urls import path
from . import views

app_name = "aura_books"

urlpatterns = [
    path("", views.book_list, name="book_list"),          # LIST
    path("create/", views.create_book, name="create_book"),    
    path("book/<int:book_id>/", views.book_reader, name="book_reader"),
    path("edit/<int:book_id>/", views.edit_book, name="edit_book"),
    path("delete/<int:book_id>/", views.delete_book, name="delete_book"),    
]
