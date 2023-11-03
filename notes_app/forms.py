from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Fieldset
from django.contrib.auth.models import User
from .models import Note


class NoteForm(forms.ModelForm):
    # content = QuillFormField()

    class Meta:
        model = Note
        fields = ['title', 'image',
                  'content']

    def __init__(self, *args, **kwargs):
        super(NoteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        # self.fields['title'].help_text = "Please select bla bla bla"

        self.fields['title'].widget.attrs['placeholder'] = 'Add a title to your note*'
        self.fields['content'].widget.attrs['placeholder'] = 'Enter your content here'
