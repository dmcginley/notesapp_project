from django import forms
from django.contrib.auth.models import User
from .models import Note


class NoteForm(forms.ModelForm):
    # content = QuillFormField()

    class Meta:
        model = Note
        fields = ['title', 'image',
                  'content']


# TODO: fix form anf add html file
