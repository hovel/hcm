from django import forms
from hcm_blog.models import Post, PostComment


class PostCreateUpdateForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'body', 'is_published', 'tags']


class PostCommentForm(forms.ModelForm):

    class Meta:
        model = PostComment
        fields = ['body', ]