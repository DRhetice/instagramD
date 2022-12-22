from django import forms
from post.models import *

class NewPostForm(forms.ModelForm):
    picture = forms.ImageField(required=True)
    caption = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Caption'}), required=True)
    tags = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Tags - separate tag with comma '}), required= True)

    class Meta:
        model= Post
        fields = ['picture', 'caption', 'tags']