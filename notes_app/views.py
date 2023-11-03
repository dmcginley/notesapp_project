from .forms import NoteForm
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic
from django.contrib.auth.models import User
import json

from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect

from .models import Note

from django.views.generic import (
    ListView, DetailView,
    CreateView, DeleteView,
    UpdateView
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
        content_data = json.loads(form.cleaned_data['content'])
        content = content_data.get('html', '')

        print(content)
        response = super().form_valid(form)

        return response


class NoteUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Note

    form_class = NoteForm
    template_name = 'notes_app/edit_note.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        note = self.get_object()
        if self.request.user == note.author:
            return True
        return False

    # def test_func(self):
    #     note = self.get_object()
    #     if self.request.user == note.author:
    #         return True
    #     return False

    # def form_valid(self, form):
    #     messages.success(self.request, 'Post updated successfully')
    #     return super().form_valid(form)


# def duplicate_note(request, note_slug):
#     try:
#         original_note = Note.objects.get(slug=note_slug)
#     except Note.DoesNotExist:
#         # Handle the case where the original note doesn't exist
#         return redirect('error_page')

#     if request.method == 'POST':
#         duplicate_form = DuplicateNoteForm(original_note, request.POST)
#         if duplicate_form.is_valid():
#             new_note = duplicate_form.save(commit=False)
#             new_note.author = request.user
#             new_note.save()
#             return redirect('note_detail', slug=new_note.slug)
#     else:
#         duplicate_form = DuplicateNoteForm(original_note)

#     return render(request, 'notes_app/duplicate_note_confirm.html', {'original_note': original_note, 'duplicate_form': duplicate_form})


class NoteDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Note
    template_name = 'notes_app/delete_note.html'
    success_url = '/'

    def test_func(self):
        note = self.get_object()
        # if self.request.user == post.author:
        if self.request.user == note.author or self.request.user.is_superuser:

            return True
        return False

    # def form_valid(self, form):
    #     messages.success(self.request, 'Post deleted.')
    #     return super().form_valid(form)
