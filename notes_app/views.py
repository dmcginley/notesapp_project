from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect

from .models import Note

from django.views.generic import (
    ListView, DetailView, CreateView
)
from .forms import NoteForm


# --------------------------------
#   note views
# --------------------------------
class NoteListView(ListView):
    """ The homepage """

    model = Note
    context_object_name = 'notes'
    # paginate_by = 6
    template_name = "notes_app/index.html"


class NoteDetailView(DetailView):
    model = Note

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    form_class = NoteForm

    template_name = "notes_app/creat_note.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
