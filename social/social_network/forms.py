from django.forms import ModelForm, CharField, ImageField, DateField, DateInput, FileInput

from .models import Message, Post
from social_authorization.models import UserProfile


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
    img = ImageField(widget=FileInput(attrs={"class": "form-control-file"}), required=False)


class ProfileForm(ModelForm):

    class Meta:
        model = UserProfile
        fields = ['birthday', 'city', 'gender', 'bio', 'occupation', 'avatar']

    birthday = DateField(input_formats=['%d/%m/%Y'], widget=DateInput(format='%d/%m/%Y'), required=False)
    avatar = ImageField(widget=FileInput(attrs={"class": "form-control-file"}), required=False)
