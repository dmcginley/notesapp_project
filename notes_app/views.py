from .forms import NoteForm
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic
from django.contrib import messages
import json
from django.contrib.auth.models import User

from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect

from .models import Note, Category

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

        # Retrieve the category slug from the URL parameter
        category_slug = self.request.GET.get('category')

        if category_slug:
            # Get the category object based on the slug
            category = get_object_or_404(Category, slug=category_slug)
            form.instance.category = category

        response = super().form_valid(form)

        return response


class NoteUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Note

    form_class = NoteForm
    template_name = 'notes_app/edit_note.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Note updated successfully')
        return super().form_valid(form)

    def test_func(self):
        note = self.get_object()
        return self.request.user == note.author


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

# TODO: messages not showing up, fix, CSS also added to tey debug
    def form_valid(self, form):
        messages.success(self.request, 'Note deleted.')
        return super().form_valid(form)


# --------------------------------
#   category/folder views
# --------------------------------


def categories(request):
    all_categories = Category.objects.all()
    return {
        'all_categories': all_categories
    }


def starred_categories(request):

# Create initial categories
    # if not Category.objects.exists():
    #     Category.create(name="Projects", is_deletable=True, is_starred=True)
    #     Category.create(name="Areas", is_deletable=True,is_starred=True)
    #     Category.create(name="Resources", is_deletable=True, is_starred=True)
    #     Category.create(name="Archives", is_deletable=True, is_starred=True)

    starred_categories = Category.objects.filter(is_starred=True)
    # print('starred_categories', starred_categories)
    
    # for category in starred_categories:
    #     category.detail_url = reverse('category_detail', kwargs={'slug': category.slug})
    #     print(f"Category: {category.name}, Detail URL: {category.detail_url}")

    context = {
        'starred_categories': starred_categories
    }

    return render(request, 'notes_app/starred_categories.html', context)



def category_list(request, category_slug):

    category = get_object_or_404(Category, slug=category_slug)
    notes = Note.objects.filter(category=category)

    # Get subcategories of the current category
    subcategories = category.subcategories.all()
    # starred_categories = Category.objects.filter(is_starred=True)
    page_title = category.name

    context = {
        'notes': notes,
        'category': category,
        'subcategories': subcategories,
        # 'starred_categories': starred_categories,
        'page_title': page_title,
    }

    return render(request, 'notes_app/category_list.html', context)
