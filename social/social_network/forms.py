from django.forms import (
    ModelForm,
    CharField,
    ImageField,
    DateField,
    DateInput,
    FileInput,
    TextInput,
    Textarea,
)


from .models import Message, Post, Comment
from social_authorization.models import UserProfile


class MessageForm(ModelForm):

    class Meta:
        model = Message
        fields = "text",

    text = CharField(widget=TextInput(attrs={"placeholder": "Your message..."}), max_length=400, label="")


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = "text",

    text = CharField(widget=Textarea(attrs={"placeholder": "Your comment..."}), max_length=500, label="")


class PostCreationForm(ModelForm):

    class Meta:
        model = Post
        fields = "title", "body", "img"
        
    title = CharField(max_length=200)
    body = CharField(max_length=2000, widget=Textarea(), label="Text")
    img = ImageField(widget=FileInput(attrs={"class": "form-control-file"}), required=False)


class ProfileForm(ModelForm):

    class Meta:
        model = UserProfile
        fields = 'birthday', 'city', 'gender', 'bio', 'occupation', 'avatar'

    birthday = DateField(
        input_formats=['%d/%m/%Y'],
        widget=DateInput(format='%d/%m/%Y', attrs={"placeholder": "01/01/1999"}),
        required=False
    )
    avatar = ImageField(widget=FileInput(
        attrs={"class": "form-control-file"}),
        required=False
    )
