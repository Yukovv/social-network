from django.forms import ModelForm, CharField, ImageField

from .models import Message, Post


class MessageForm(ModelForm):

    class Meta:
        model = Message
        fields = "text",

    text = CharField(max_length=400)


class PostCreationForm(ModelForm):

    class Meta:
        model = Post
        fields = "title", "body", "img"
        
    title = CharField(max_length=400)
    body = CharField(max_length=2000, label="Text")
    img = ImageField(label="Image")
