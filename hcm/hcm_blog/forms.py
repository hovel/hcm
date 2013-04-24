from django import forms
from markitup.widgets import MarkItUpWidget
from hcm_blog.models import Post, PostComment


class PostCreateUpdateForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'body', 'is_published', 'tags']
        widgets = {
            'body': MarkItUpWidget()
        }


class PostCommentForm(forms.ModelForm):

    class Meta:
        model = PostComment
        fields = ['body', ]