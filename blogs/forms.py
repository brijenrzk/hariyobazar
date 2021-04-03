from django import forms
from .models import *
from ckeditor.widgets import CKEditorWidget


class CreateBlogForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Blogs
        fields = ['title', 'photo', 'description']
