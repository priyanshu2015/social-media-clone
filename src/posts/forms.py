from django.forms import Form, ModelForm
from .models import Post
from django import forms


class UploadPostForm(ModelForm):
    # "react,aws,system_design"
    tags = forms.CharField(required=False)

    class Meta:
        model = Post
        fields = [
            "image",
            "caption"
        ]


class PostCommentForm(forms.Form):
    comment_detail = forms.CharField(max_length=500)