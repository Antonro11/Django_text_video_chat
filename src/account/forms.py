from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "photo", "password1", "password2")