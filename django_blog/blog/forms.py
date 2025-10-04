from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post
from .models import Comment
from taggit.forms import TagWidget


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email"]

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]
        widgets = {
            'tags': TagWidget(attrs={'placeholder': 'Add tags separated by commas'}),
        }

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={"rows": 3, "placeholder": "Write a comment..."})
    )

    class Meta:
        model = Comment
        fields = ["content"]