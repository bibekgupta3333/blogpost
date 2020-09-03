from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Post


class PostForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Post
        fields = ['title',  'image', 'body', 'status', 'tags']
        required = {
            'author': False
        }

    def __init__(self,  *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True, *args, **kwargs):
        obj = super(PostForm, self).save(commit=False, *args, **kwargs)

        from django.utils.text import slugify
        obj.slug = slugify(obj.title)
        if commit:
            obj.save()
        return obj


class PostCreateForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Post
        fields = ['title', 'author', 'image', 'body', 'status', 'tags']

    def __init__(self,  *args, **kwargs):
        super(PostCreateForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class': 'form-control'})
        self.fields['author'].widget.attrs.update({'style': 'display:none;'})
        self.fields['author'].label = ''
