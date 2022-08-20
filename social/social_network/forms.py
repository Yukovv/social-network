from django.forms import ModelForm, CharField

from .models import Message


class MessageForm(ModelForm):

    class Meta:
        model = Message
        fields = "text",

    text = CharField(max_length=400)
