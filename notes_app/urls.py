from django.urls import path, include
from . import views


from .views import NoteListView, NoteDetailView, NoteCreateView


urlpatterns = [
    path('', NoteListView.as_view(), name='home'),
    path('note/<slug:slug>/', NoteDetailView.as_view(), name='note_detail'),
    path('creat-note/', NoteCreateView.as_view(), name='creat_note'),

]
