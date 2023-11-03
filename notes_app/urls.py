from django.urls import path, include
from . import views


from .views import (NoteListView, NoteDetailView,
                    NoteCreateView, NoteUpdateView,
                    NoteDeleteView)


urlpatterns = [
    path('', NoteListView.as_view(), name='home'),
    path('note/<slug:slug>/', NoteDetailView.as_view(), name='note_detail'),
    path('creat-note/', NoteCreateView.as_view(), name='creat_note'),
    path('edit-note/<slug:slug>/', NoteUpdateView.as_view(), name='edit_note'),
    path('delete-note/<slug:slug>/', NoteDeleteView.as_view(),
         name='delete_note'),
]
