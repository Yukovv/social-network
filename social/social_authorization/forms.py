from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm as UserForm, AuthenticationForm
from django.forms import EmailField


class UserCreationForm(UserForm):

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email')

    email = EmailField(
        required=True,
        max_length=200,
        help_text="Required."
    )
