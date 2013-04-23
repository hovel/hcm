from django import forms
from hcm_blog.models import Post


class PostCreateUpdateForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'body', 'is_published', 'tags']